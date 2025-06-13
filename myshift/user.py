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

from typing import Dict, Any
from pdpyras import APISession

def get_user_id_by_email(session: APISession, email: str) -> str:
    users = session.rget('/users', params={'query': email})
    for user in users.get('users', []):
        if user.get('email', '').lower() == email.lower():
            return user.get('id')
    import sys
    print(f"User with email {email} not found in PagerDuty.", file=sys.stderr)
    sys.exit(1)

def get_user_name_by_id(session: APISession, user_id: str) -> str:
    user = session.rget(f'/users/{user_id}')
    return user.get('user', {}).get('name', user_id) 