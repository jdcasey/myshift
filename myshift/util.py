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
from pdpyras import APISession

def get_pd_session(config: Dict[str, Any]) -> APISession:
    api_token = config.get('pagerduty_token')
    base_url = config.get('pagerduty_base_url', 'https://api.pagerduty.com')
    if not api_token:
        print('pagerduty_token missing in spre-config.yaml', file=sys.stderr)
        sys.exit(1)
    return APISession(api_token, default_from_email=None, api_url=base_url)

def resolve_schedule_id(parsed_args: Any, config: Dict[str, Any]) -> str:
    schedule_id = getattr(parsed_args, 'schedule_id', None) or config.get('schedule_id')
    if not schedule_id:
        print('Schedule ID must be specified either as a command line argument or in the configuration file (schedule_id).', file=sys.stderr)
        sys.exit(2)
    return schedule_id 