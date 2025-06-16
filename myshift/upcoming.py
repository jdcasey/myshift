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
from typing import Optional, List, Dict, Any, Set, Tuple
from datetime import datetime, timedelta
from dateutil import tz
from myshift.config import load_config
from myshift.util import get_pd_session, resolve_schedule_id, get_user_id_by_email, get_user_name_by_id
import yaml

def upcoming_main(args: Optional[List[str]] = None, config: Optional[Dict[str, Any]] = None) -> None:
    parser = argparse.ArgumentParser(description='Show upcoming on-call shifts for a user.')
    parser.add_argument('schedule_id', nargs='?', help='PagerDuty schedule ID to check')
    group = parser.add_mutually_exclusive_group(required=False)  # Changed to not required since we can use config
    group.add_argument('--user-id', help='PagerDuty user ID to check (overrides my_user from config)')
    group.add_argument('--user-email', help='PagerDuty user email to check (overrides my_user from config)')
    parser.add_argument('--weeks', type=int, default=4, help='Number of weeks to look ahead (default: 4)')
    parsed_args = parser.parse_args(args)

    if config is None:
        config = load_config()

    # Check if we have a user specified either via args or config
    if not (parsed_args.user_id or parsed_args.user_email or config.get('my_user')):
        print("No user specified. Either use --user-id/--user-email or set my_user in config.", file=sys.stderr)
        sys.exit(2)

    schedule_id = resolve_schedule_id(parsed_args, config)
    session = get_pd_session(config)

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

    user_name = get_user_name_by_id(session, user_id)
    now = datetime.utcnow()
    end_date = now + timedelta(weeks=parsed_args.weeks)
    
    params = {
        'since': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'until': end_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'user_ids': [user_id],
        'schedule_ids': [schedule_id],
        'overflow': 'true'
    }
    
    shifts = session.rget(f'/oncalls', params=params)
    
    # Use a set to track unique shifts by start and end time
    unique_shifts: Set[Tuple[datetime, datetime]] = set()
    utc = tz.tzutc()
    local_tz = tz.tzlocal()
    
    for shift in shifts:
        # Convert UTC times to local timezone
        start_utc = datetime.strptime(shift['start'], '%Y-%m-%dT%H:%M:%SZ')
        end_utc = datetime.strptime(shift['end'], '%Y-%m-%dT%H:%M:%SZ')
        
        start_local = start_utc.replace(tzinfo=utc).astimezone(local_tz)
        end_local = end_utc.replace(tzinfo=utc).astimezone(local_tz)
        
        # Add to set of unique shifts
        unique_shifts.add((start_local, end_local))
    
    if not unique_shifts:
        print(f"No upcoming shifts found for {user_name} ({user_id}) in the next {parsed_args.weeks} weeks.")
        return
    
    print(f"Upcoming on-call shifts for {user_name} ({user_id}) in the next {parsed_args.weeks} weeks:")
    # Sort shifts by start time
    for start, end in sorted(unique_shifts):
        # Format times as requested
        day = start.strftime('%Y-%m-%d')
        start_str = start.strftime('%H:%M')
        end_str = end.strftime('%H:%M')
        
        print(f"  {day}: {start_str} to {end_str}") 