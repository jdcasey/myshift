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

import os
import sys
from typing import Any, Dict, Optional
from pagerduty import RestApiV2Client

def get_pd_session(config: Dict[str, Any]) -> RestApiV2Client:
    api_token = config.get('pagerduty_token')
    if not api_token:
        print('pagerduty_token missing in myshift.yaml', file=sys.stderr)
        sys.exit(1)
    
    return RestApiV2Client(api_token)

def resolve_schedule_id(parsed_args: Any, config: Dict[str, Any]) -> str:
    schedule_id = getattr(parsed_args, 'schedule_id', None) or config.get('schedule_id')
    if not schedule_id:
        print('Schedule ID must be specified either as a command line argument or in the configuration file (schedule_id).', file=sys.stderr)
        sys.exit(2)
    return schedule_id 

def get_user_id_by_email(session: RestApiV2Client, email: str) -> str:
    user = session.find('users', email, attribute='email')
    if not user:
        print(f"User with email {email} not found in PagerDuty.", file=sys.stderr)
        sys.exit(1) 

    return user['id']

def get_user_name_by_id(session: RestApiV2Client, user_id: str) -> str:
    user = session.rget(f"/users/{user_id}")

    if not user:
        print(f"User with ID {user_id} not found in PagerDuty.", file=sys.stderr)
        sys.exit(1) 

    return user['name'] 