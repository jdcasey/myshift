# Copyright 2025 John Casey
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import sys
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, timedelta
from myshift.config import load_config
from myshift.util import get_pd_session, resolve_schedule_id
from myshift.user import get_user_id_by_email, get_user_name_by_id

def get_consecutive_target_shifts(session: Any, schedule_id: str, target_user_id: str, start_date: datetime) -> List[Dict[str, str]]:
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

def print_sample_config() -> None:
    import yaml
    sample = {
        'pagerduty_token': 'PASTE_YOUR_PD_API_TOKEN_HERE',
        'pagerduty_base_url': 'https://api.pagerduty.com'
    }
    print(yaml.dump(sample, default_flow_style=False).rstrip())
    print('# schedule_id: PASTE_YOUR_SCHEDULE_ID_HERE')

def override_main(args: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description='Override PagerDuty schedule rotations for a sequence of days.')
    parser.add_argument('schedule_id', nargs='?', help='PagerDuty schedule ID to override')
    parser.add_argument('--start-date', required=False, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', required=False, help='End date (YYYY-MM-DD, inclusive)')
    assign_group = parser.add_mutually_exclusive_group(required=False)
    assign_group.add_argument('--user-id', help='PagerDuty user ID to assign for the override')
    assign_group.add_argument('--user-email', help='PagerDuty user email to assign for the override')
    target_group = parser.add_mutually_exclusive_group(required=False)
    target_group.add_argument('--target-user-id', help='PagerDuty user ID whose shifts will be overridden')
    target_group.add_argument('--target-user-email', help='PagerDuty user email whose shifts will be overridden')
    parser.add_argument('--print-sample-config', action='store_true', help='Print a sample spre-config.yaml and exit')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be overridden, but do not make any changes')
    parsed_args = parser.parse_args(args)

    if parsed_args.print_sample_config:
        print_sample_config()
        sys.exit(0)

    config = load_config()

    # Determine schedule_id
    schedule_id = resolve_schedule_id(parsed_args, config)

    # Check required arguments if not printing sample config
    if not ((parsed_args.user_id or parsed_args.user_email) and (parsed_args.target_user_id or parsed_args.target_user_email) and parsed_args.start_date):
        print("Missing required arguments. See --help.", file=sys.stderr)
        sys.exit(2)

    session = get_pd_session(config)

    # Determine user_id (to assign)
    if parsed_args.user_id:
        user_id = parsed_args.user_id
    else:
        user_id = get_user_id_by_email(session, parsed_args.user_email)

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