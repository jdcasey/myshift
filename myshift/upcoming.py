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
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from myshift.config import load_config
from myshift.util import get_pd_session, resolve_schedule_id
from myshift.user import get_user_id_by_email, get_user_name_by_id

def upcoming_main(args: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description='Show upcoming on-call shifts for a user.')
    parser.add_argument('schedule_id', nargs='?', help='PagerDuty schedule ID to check')
    parser.add_argument('--weeks', type=int, default=4, help='Number of weeks to look ahead (default: 4)')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--user-id', help='PagerDuty user ID to check')
    group.add_argument('--user-email', help='PagerDuty user email to check')
    parsed_args = parser.parse_args(args)

    config = load_config()
    schedule_id = resolve_schedule_id(parsed_args, config)
    session = get_pd_session(config)

    if parsed_args.user_id:
        user_id = parsed_args.user_id
    else:
        user_id = get_user_id_by_email(session, parsed_args.user_email)

    user_name = get_user_name_by_id(session, user_id)
    now = datetime.utcnow()
    end = now + timedelta(weeks=parsed_args.weeks)
    params = {
        'since': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'until': end.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'overflow': 'true'
    }
    resp = session.rget(f'/schedules/{schedule_id}/users/{user_id}/on_call', params=params)
    shifts = resp.get('oncalls', [])
    if not shifts:
        print(f"No upcoming shifts found for {user_name} ({user_id}) in the next {parsed_args.weeks} week(s).")
        return
    print(f"Upcoming on-call shifts for {user_name} ({user_id}):")
    for shift in shifts:
        print(f"  {shift['start']} to {shift['end']}") 