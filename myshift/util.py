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

"""Utility functions for interacting with the PagerDuty API and managing on-call schedules.

This module provides core functionality for:
- PagerDuty API authentication and session management
- Schedule ID resolution from command line args or config
- User identification and information retrieval
- Shift retrieval and management
- User mapping and data organization

All datetime operations handle timezone conversion between UTC and local time.
"""

import os
import sys
from typing import Any, Dict, Optional, Set, Tuple, List
from datetime import datetime, timezone
from dateutil import tz
from pagerduty import RestApiV2Client

def get_pd_session(config: Dict[str, Any]) -> RestApiV2Client:
    """Create an authenticated PagerDuty API session.
    
    Args:
        config: Configuration dictionary containing pagerduty_token
        
    Returns:
        Authenticated PagerDuty API client
        
    Raises:
        SystemExit: If pagerduty_token is missing from config
    """
    api_token = config.get('pagerduty_token')
    if not api_token:
        print('pagerduty_token missing in myshift.yaml', file=sys.stderr)
        sys.exit(1)
    
    return RestApiV2Client(api_token)

def resolve_schedule_id(parsed_args: Any, config: Dict[str, Any]) -> str:
    """Resolve schedule ID from command line arguments or configuration.
    
    Args:
        parsed_args: Command line arguments object
        config: Configuration dictionary
        
    Returns:
        Schedule ID string
        
    Raises:
        SystemExit: If schedule_id is not found in either source
    """
    schedule_id = getattr(parsed_args, 'schedule_id', None) or config.get('schedule_id')
    if not schedule_id:
        print('Schedule ID must be specified either as a command line argument or in the configuration file (schedule_id).', file=sys.stderr)
        sys.exit(2)
    return schedule_id 

def get_user_id_by_email(session: RestApiV2Client, email: str) -> str:
    """Get PagerDuty user ID from email address.
    
    Args:
        session: PagerDuty API session
        email: User's email address
        
    Returns:
        User ID string
        
    Raises:
        SystemExit: If user is not found
    """
    user = session.find('users', email, attribute='email')
    if not user:
        print(f"User with email {email} not found in PagerDuty.", file=sys.stderr)
        sys.exit(1) 

    return user['id']

def get_user_name_by_id(session: RestApiV2Client, user_id: str) -> str:
    """Get PagerDuty user's full name from their ID.
    
    Args:
        session: PagerDuty API session
        user_id: User's PagerDuty ID
        
    Returns:
        User's full name
        
    Raises:
        SystemExit: If user is not found
    """
    user = session.rget(f"/users/{user_id}")

    if not user:
        print(f"User with ID {user_id} not found in PagerDuty.", file=sys.stderr)
        sys.exit(1) 

    return user['name'] 

def get_unique_shifts(session: RestApiV2Client, user_id: str, schedule_id: str, until: datetime) -> List[Tuple[datetime, datetime]]:
    """Get unique on-call shifts for a user in a schedule.
    
    Args:
        session: PagerDuty API session
        user_id: PagerDuty user ID
        schedule_id: PagerDuty schedule ID
        until: End datetime for the search range
        
    Returns:
        List of tuples containing (start_time, end_time) in local timezone.
        Times are sorted chronologically.
    """
    now = datetime.now(timezone.utc)
    
    params = {
        'since': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'until': until.strftime('%Y-%m-%dT%H:%M:%SZ'),
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
    
    return sorted(unique_shifts) 

def get_all_unique_shifts(session: RestApiV2Client, schedule_id: str, until: datetime, target_tz: Optional[datetime.tzinfo] = None) -> List[Tuple[datetime, datetime, str]]:
    """Get all unique on-call shifts in a schedule with user information.
    
    Args:
        session: PagerDuty API session
        schedule_id: PagerDuty schedule ID
        until: End datetime for the search range
        target_tz: Target timezone for the output times (defaults to local timezone)
        
    Returns:
        List of tuples containing (start_time, end_time, user_id) in target timezone.
        Times are sorted chronologically.
    """
    now = datetime.now(timezone.utc)
    
    params = {
        'since': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'until': until.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'schedule_ids': [schedule_id],
        'overflow': 'true'
    }
    
    shifts = session.rget(f'/oncalls', params=params)
    
    # Use a set to track unique shifts by start, end time, and user
    unique_shifts: Set[Tuple[datetime, datetime, str]] = set()
    utc = tz.tzutc()
    if target_tz is None:
        target_tz = tz.tzlocal()
    
    for shift in shifts:
        user = shift.get('user', {})
        user_id = user.get('id', 'Unknown')
        
        # Convert UTC times to target timezone
        start_utc = datetime.strptime(shift['start'], '%Y-%m-%dT%H:%M:%SZ')
        end_utc = datetime.strptime(shift['end'], '%Y-%m-%dT%H:%M:%SZ')
        
        start_local = start_utc.replace(tzinfo=utc).astimezone(target_tz)
        end_local = end_utc.replace(tzinfo=utc).astimezone(target_tz)
        
        # Add to set of unique shifts with user info
        unique_shifts.add((start_local, end_local, user_id))
    
    return sorted(unique_shifts) 

def build_user_map(session: RestApiV2Client, schedule_entries: List[Tuple[datetime, datetime, str]]) -> Dict[str, Dict]:
    """Build a map of user objects from schedule entries.

    This function builds a map of all user objects referenced in the given schedule entries
    by collecting unique user IDs and then fetching the full user objects in a single request.

    Args:
        session: PagerDuty API session
        schedule_entries: List of tuples containing (start_time, end_time, user_id)

    Returns:
        Dictionary mapping user IDs to their full user objects.
        Each user object contains all PagerDuty user information.
    """

    user_map = {}
    for uid in [entry[2] for entry in schedule_entries if entry[2]]:
        user = session.rget(f"/users/{uid}")
        if user:
            user_map[uid] = user
    
    return user_map