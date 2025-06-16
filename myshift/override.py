"""Override management for PagerDuty on-call schedules.

This module provides functionality to override existing on-call shifts in PagerDuty,
allowing users to:
- Override consecutive shifts for a target user
- Assign overrides to a specific user
- Preview changes with dry-run mode
"""

import argparse
import sys
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, timedelta
from myshift.config import load_config
from myshift.util import get_pd_session, resolve_schedule_id, get_user_id_by_email, get_user_name_by_id

def get_consecutive_target_shifts(session: Any, schedule_id: str, target_user_id: str, start_date: datetime) -> List[Dict[str, str]]:
    """Get consecutive shifts for a target user starting from a specific date.
    
    This function looks for consecutive shifts up to 30 days in the future.
    It stops when it finds a day without a shift or when it reaches the maximum days.
    
    Args:
        session: PagerDuty API session
        schedule_id: Schedule ID to check
        target_user_id: User ID whose shifts to get
        start_date: Date to start looking for shifts
        
    Returns:
        List of dictionaries containing shift information:
        - start: ISO format start time
        - end: ISO format end time
    """
    max_days = 30
    current_date = start_date
    shifts = []
    for _ in range(max_days):
        day_start = current_date.strftime('%Y-%m-%dT00:00:00Z')
        day_end = (current_date + timedelta(days=1)).strftime('%Y-%m-%dT00:00:00Z')
        params = {'since': day_start, 'until': day_end, 'overflow': 'true'}
        resp = session.rget(f'/schedules/{schedule_id}/users/{target_user_id}/on_call', params=params)
        if not resp.get('oncalls'):
            break
        for oc in resp['oncalls']:
            if oc.get('user', {}).get('id') == target_user_id:
                shifts.append({
                    'start': oc['start'],
                    'end': oc['end']
                })
                break
        else:
            break
        current_date += timedelta(days=1)
    return shifts

def override_main(args: Optional[List[str]] = None, config: Optional[Dict[str, Any]] = None) -> None:
    """Main entry point for the override command.
    
    This function handles the override sub-command, allowing users to:
    1. Override consecutive shifts for a target user
    2. Assign those shifts to another user
    3. Preview changes with dry-run mode
    
    Command-line arguments:
        schedule_id: Optional PagerDuty schedule ID to override
        --start-date: Required start date (YYYY-MM-DD)
        --end-date: Optional end date (YYYY-MM-DD, inclusive)
        --user-id: Optional user ID to assign (overrides my_user from config)
        --user-email: Optional user email to assign (overrides my_user from config)
        --target-user-id: Optional target user ID whose shifts will be overridden
        --target-user-email: Optional target user email whose shifts will be overridden
        --dry-run: Optional flag to preview changes without making them
    
    Args:
        args: Optional command line arguments
        config: Optional configuration dictionary
        
    Raises:
        SystemExit: If required arguments are missing or if API calls fail
    """
    parser = argparse.ArgumentParser(description='Override PagerDuty schedule rotations for a sequence of days.')
    parser.add_argument('schedule_id', nargs='?', help='PagerDuty schedule ID to override')
    parser.add_argument('--start-date', required=False, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', required=False, help='End date (YYYY-MM-DD, inclusive)')
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--user-id', help='PagerDuty user ID to assign (overrides my_user from config)')
    group.add_argument('--user-email', help='PagerDuty user email to assign (overrides my_user from config)')
    target_group = parser.add_mutually_exclusive_group(required=False)
    target_group.add_argument('--target-user-id', help='PagerDuty user ID whose shifts will be overridden')
    target_group.add_argument('--target-user-email', help='PagerDuty user email whose shifts will be overridden')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be overridden, but do not make any changes')
    parsed_args = parser.parse_args(args)

    if config is None:
        config = load_config()

    # Determine schedule_id
    schedule_id = resolve_schedule_id(parsed_args, config)

    # Check required arguments if not printing sample config
    if not ((parsed_args.user_id or parsed_args.user_email or config.get('my_user')) and 
            (parsed_args.target_user_id or parsed_args.target_user_email) and 
            parsed_args.start_date):
        print("Missing required arguments. See --help.", file=sys.stderr)
        sys.exit(2)

    session = get_pd_session(config)

    # Determine user_id (to assign)
    if parsed_args.user_id:
        user_id = parsed_args.user_id
    elif parsed_args.user_email:
        user_id = get_user_id_by_email(session, parsed_args.user_email)
    else:
        # Use my_user from config
        my_user = config.get('my_user')
        if '@' in my_user:
            user_id = get_user_id_by_email(session, my_user)
        else:
            user_id = my_user

    # Determine target_user_id (whose shifts will be overridden)
    if parsed_args.target_user_id:
        target_user_id = parsed_args.target_user_id
    else:
        target_user_id = get_user_id_by_email(session, parsed_args.target_user_email)

    start_date = datetime.strptime(parsed_args.start_date, '%Y-%m-%d')

    # Always use scheduled shift times for the target user
    shifts = get_consecutive_target_shifts(session, schedule_id, target_user_id, start_date)
    overridden_shifts = []
    if not shifts:
        print(f"No consecutive shifts found for user {target_user_id} starting from {parsed_args.start_date}", file=sys.stderr)
    else:
        overriding_user_name = get_user_name_by_id(session, user_id)
        target_user_name = get_user_name_by_id(session, target_user_id)
        if parsed_args.dry_run:
            print(f"DRY RUN: The following shifts would be overridden:")
            print(f"  Target user: {target_user_name} ({target_user_id})")
            print(f"  Overriding user: {overriding_user_name} ({user_id})")
            for shift in shifts:
                print(f"    {shift['start']} to {shift['end']}")
        else:
            for shift in shifts:
                override = {
                    'override': {
                        'start': shift['start'],
                        'end': shift['end'],
                        'user_id': user_id
                    }
                }
                print(f"Creating override for {shift['start']} to {shift['end']} for user {user_id}")
                resp = session.rpost(f'/schedules/{schedule_id}/overrides', json=override)
                if 'override' in resp:
                    print(f"Override created: {resp['override']['id']}")
                    overridden_shifts.append((shift['start'], shift['end']))
                else:
                    print(f"Failed to create override for {shift['start']}", file=sys.stderr)
                    print(resp, file=sys.stderr)
    # Print summary
    if not parsed_args.dry_run:
        if overridden_shifts:
            print("\nShifts overridden:")
            for start, end in overridden_shifts:
                print(f"  {start} to {end}")
        else:
            print("No shifts were overridden.") 