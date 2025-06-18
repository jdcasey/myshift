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

import argparse
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple, TypedDict

from dateutil import tz
from pagerduty import RestApiV2Client, HttpError, UrlError


class UserObject(TypedDict):
    """Type definition for PagerDuty user objects."""

    id: str
    name: str
    email: str


def get_pd_session(config: Dict[str, Any]) -> RestApiV2Client:
    """Create an authenticated PagerDuty API session.

    Args:
        config: Configuration dictionary containing pagerduty_token

    Returns:
        Authenticated PagerDuty API client

    Raises:
        SystemExit: If pagerduty_token is missing from config
    """
    api_token = config.get("pagerduty_token")
    if not api_token:
        print("pagerduty_token missing in myshift.yaml", file=sys.stderr)
        sys.exit(1)

    # Configure client with modern settings
    client = RestApiV2Client(api_token)
    
    # Set reasonable retry limits for better reliability
    client.max_http_attempts = 3
    client.sleep_timer = 2.0
    client.sleep_timer_base = 2
    
    # Enable debug mode if needed (disabled by default)
    # client.print_debug = True
    
    return client


def resolve_schedule_id(parsed_args: argparse.Namespace, config: Dict[str, Any]) -> str:
    """Resolve schedule ID from command line arguments or configuration.

    Args:
        parsed_args: Command line arguments object
        config: Configuration dictionary

    Returns:
        Schedule ID string

    Raises:
        SystemExit: If schedule_id is not found in either source
    """
    schedule_id = getattr(parsed_args, "schedule_id", None) or config.get("schedule_id")
    if not schedule_id:
        print(
            "Schedule ID must be specified either as a command line argument "
            "or in the configuration file (schedule_id).",
            file=sys.stderr,
        )
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
        SystemExit: If user is not found or API error occurs
    """
    try:
        user = session.find("users", email, attribute="email")
        if not user:
            print(f"User with email {email} not found in PagerDuty.", file=sys.stderr)
            sys.exit(1)
        return user["id"]
        
    except HttpError as e:
        if e.response.status_code == 404:
            print(f"User with email {email} not found in PagerDuty.", file=sys.stderr)
        else:
            print(f"PagerDuty API error: {e.response.status_code} - {e}", file=sys.stderr)
        sys.exit(1)
    except UrlError as e:
        print(f"Invalid API request: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error looking up user: {e}", file=sys.stderr)
        sys.exit(1)


def get_user_name_by_id(session: RestApiV2Client, user_id: str) -> str:
    """Get PagerDuty user's full name from their ID.

    Args:
        session: PagerDuty API session
        user_id: User's PagerDuty ID

    Returns:
        User's full name

    Raises:
        SystemExit: If user is not found or API error occurs
    """
    try:
        user = session.rget(f"/users/{user_id}")
        if not user:
            print(f"User with ID {user_id} not found in PagerDuty.", file=sys.stderr)
            sys.exit(1)
        return user["name"]
        
    except HttpError as e:
        if e.response.status_code == 404:
            print(f"User with ID {user_id} not found in PagerDuty.", file=sys.stderr)
        else:
            print(f"PagerDuty API error: {e.response.status_code} - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error looking up user: {e}", file=sys.stderr)
        sys.exit(1)


def get_unique_shifts(
    session: RestApiV2Client,
    user_id: str,
    schedule_id: str,
    until: datetime,
) -> List[Tuple[datetime, datetime]]:
    """Get unique on-call shifts for a user in a schedule.

    Args:
        session: PagerDuty API session
        user_id: PagerDuty user ID
        schedule_id: PagerDuty schedule ID
        until: End datetime for the search range

    Returns:
        List of tuples containing (start_time, end_time) in local timezone.
        Times are sorted chronologically.

    Raises:
        SystemExit: If API calls fail
    """
    try:
        now = datetime.now(timezone.utc)

        params = {
            "since": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "until": until.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "user_ids": [user_id],
            "schedule_ids": [schedule_id],
            "overflow": "true",
        }

        print(f"Fetching shifts from {params['since']} to {params['until']}")

        # Use modern iter_all for automatic pagination
        all_shifts = list(session.iter_all("/oncalls", params=params))
        print(f"Got {len(all_shifts)} shifts from API")

        # Use a set to track unique shifts by start and end time
        unique_shifts: Set[Tuple[datetime, datetime]] = set()
        utc = tz.tzutc()
        local_tz = tz.tzlocal()

        for shift in all_shifts:
            # Convert UTC times to local timezone
            start_utc = datetime.strptime(shift["start"], "%Y-%m-%dT%H:%M:%SZ")
            end_utc = datetime.strptime(shift["end"], "%Y-%m-%dT%H:%M:%SZ")

            start_local = start_utc.replace(tzinfo=utc).astimezone(local_tz)
            end_local = end_utc.replace(tzinfo=utc).astimezone(local_tz)

            # Add to set of unique shifts
            unique_shifts.add((start_local, end_local))

        print(f"Found {len(unique_shifts)} unique shifts")
        return sorted(unique_shifts)
        
    except HttpError as e:
        print(f"PagerDuty API error fetching shifts: {e.response.status_code} - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error fetching shifts: {e}", file=sys.stderr)
        sys.exit(1)


def get_all_unique_shifts(
    session: RestApiV2Client,
    schedule_id: str,
    until: datetime,
    target_tz: Optional[datetime.tzinfo] = None,
) -> List[Tuple[datetime, datetime, str]]:
    """Get all unique on-call shifts in a schedule with user information.

    Args:
        session: PagerDuty API session
        schedule_id: PagerDuty schedule ID
        until: End datetime for the search range
        target_tz: Optional timezone to convert times to

    Returns:
        List of tuples containing (start_time, end_time, user_id) in target timezone.
        Times are sorted chronologically.

    Raises:
        SystemExit: If API calls fail
    """
    try:
        now = datetime.now(timezone.utc)
        target_tz = target_tz or tz.tzlocal()

        params = {
            "since": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "until": until.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "schedule_ids": [schedule_id],
            "overflow": "true",
        }

        print(f"Fetching shifts from {params['since']} to {params['until']}")

        # Use modern iter_all for automatic pagination - much cleaner!
        all_shifts = list(session.iter_all("/oncalls", params=params))
        print(f"Got {len(all_shifts)} shifts from API")

        # Use a set to track unique shifts by start, end time, and user
        unique_shifts: Set[Tuple[datetime, datetime, str]] = set()
        utc = tz.tzutc()

        for shift in all_shifts:
            # Convert UTC times to target timezone
            start_utc = datetime.strptime(shift["start"], "%Y-%m-%dT%H:%M:%SZ")
            end_utc = datetime.strptime(shift["end"], "%Y-%m-%dT%H:%M:%SZ")

            start_local = start_utc.replace(tzinfo=utc).astimezone(target_tz)
            end_local = end_utc.replace(tzinfo=utc).astimezone(target_tz)

            # Add to set of unique shifts
            unique_shifts.add((start_local, end_local, shift["user"]["id"]))

        print(f"Found {len(unique_shifts)} unique shifts")
        return sorted(unique_shifts)
        
    except HttpError as e:
        print(f"PagerDuty API error fetching shifts: {e.response.status_code} - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error fetching shifts: {e}", file=sys.stderr)
        sys.exit(1)


def build_user_map(
    session: RestApiV2Client,
    schedule_entries: List[Tuple[datetime, datetime, str]],
) -> Dict[str, UserObject]:
    """Build a mapping of user IDs to user information.

    Args:
        session: PagerDuty API session
        schedule_entries: List of (start_time, end_time, user_id) tuples

    Returns:
        Dictionary mapping user IDs to user information

    Raises:
        SystemExit: If API calls fail
    """
    try:
        user_map: Dict[str, UserObject] = {}
        user_ids = {entry[2] for entry in schedule_entries}

        # More efficient: fetch all users with include parameter
        # This is better than individual API calls for each user
        if user_ids:
            # Convert to list for API call
            user_id_list = list(user_ids)
            
            # Use list_all for better performance with large user sets
            all_users = session.list_all(
                "users", 
                params={
                    "ids": user_id_list,
                    "include": ["contact_methods", "notification_rules"]
                }
            )
            
            for user in all_users:
                if user["id"] in user_ids:
                    user_map[user["id"]] = {
                        "id": user["id"],
                        "name": user["name"],
                        "email": user["email"],
                    }

        # Fallback: for any missing users, fetch individually
        missing_users = user_ids - set(user_map.keys())
        for user_id in missing_users:
            try:
                user = session.rget(f"/users/{user_id}")
                if user:
                    user_map[user_id] = {
                        "id": user["id"],
                        "name": user["name"],
                        "email": user["email"],
                    }
            except HttpError as e:
                if e.response.status_code == 404:
                    print(f"Warning: User {user_id} not found, skipping", file=sys.stderr)
                else:
                    raise

        return user_map
        
    except HttpError as e:
        print(f"PagerDuty API error building user map: {e.response.status_code} - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error building user map: {e}", file=sys.stderr)
        sys.exit(1)
