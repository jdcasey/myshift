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
from datetime import datetime
from myshift.config import load_config
from myshift.util import get_pd_session, resolve_schedule_id
from myshift.user import get_user_id_by_email, get_user_name_by_id

def next_main(args: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description='Show the next on-call shift for a user.')
    parser.add_argument('schedule_id', nargs='?', help='PagerDuty schedule ID to check')
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
    
    # Get the next shift by querying from now until a reasonable future date (e.g., 1 year)
    params = {
        'since': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'until': (now.replace(year=now.year + 1)).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'overflow': 'true'
    }
    
    resp = session.rget(f'/schedules/{schedule_id}/users/{user_id}/on_call', params=params)
    shifts = resp.get('oncalls', [])
    
    if not shifts:
        print(f"No upcoming shifts found for {user_name} ({user_id}).")
        return
    
    # The first shift in the response is the next one
    next_shift = shifts[0]
    print(f"Next on-call shift for {user_name} ({user_id}):")
    print(f"  {next_shift['start']} to {next_shift['end']}") 