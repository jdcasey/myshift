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

"""Next shift management for PagerDuty on-call schedules.

This module provides functionality to view the next upcoming on-call shift for a user,
including:
- Finding the next scheduled shift within a 3-month window
- Filtering shifts by user (via ID or email)
- Displaying shift details in a user-friendly format
"""

import sys
from datetime import datetime, timedelta
from typing import Optional

from dateutil import tz
from pagerduty import RestApiV2Client

from myshift.util import get_unique_shifts, get_user_id_by_email


def next_shift(
    session: RestApiV2Client,
    schedule_id: str,
    email: Optional[str] = None,
    days: int = 90,
) -> None:
    """Show the next on-call shift for a user.

    Args:
        session: PagerDuty API session
        schedule_id: PagerDuty schedule ID
        email: Optional email address to look up user ID
        days: Number of days to look ahead

    Raises:
        SystemExit: If email is not provided or API calls fail
    """
    if not email:
        print("Email address is required", file=sys.stderr)
        sys.exit(1)

    try:
        user_id = get_user_id_by_email(session, email)
        until = datetime.now(tz.tzlocal()) + timedelta(days=days)

        shifts = get_unique_shifts(session, user_id, schedule_id, until)
        if not shifts:
            print("No upcoming shifts found")
            return

        next_shift_start, next_shift_end = shifts[0]
        now = datetime.now(tz.tzlocal())

        if next_shift_start <= now <= next_shift_end:
            print("Currently on call")
            print(f"Shift ends: {next_shift_end.strftime('%Y-%m-%d %H:%M %Z')}")
        elif next_shift_start > now:
            print("Next shift:")
            print(f"Starts: {next_shift_start.strftime('%Y-%m-%d %H:%M %Z')}")
            print(f"Ends: {next_shift_end.strftime('%Y-%m-%d %H:%M %Z')}")
        else:
            print("No upcoming shifts found")
    except Exception as e:
        print(f"Error fetching shift information: {e}", file=sys.stderr)
        sys.exit(1)
