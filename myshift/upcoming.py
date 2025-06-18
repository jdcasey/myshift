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

"""Upcoming shifts management for PagerDuty on-call schedules.

This module provides functionality to view upcoming on-call shifts for a user,
including:
- Listing all upcoming shifts within a specified time window
- Filtering shifts by user (via ID or email)
- Configurable look-ahead period
"""

import sys
from datetime import datetime, timedelta
from typing import Dict, Optional

from dateutil import tz
from pagerduty import RestApiV2Client

from myshift.util import get_unique_shifts, get_user_id_by_email


def upcoming_shifts(
    session: RestApiV2Client,
    schedule_id: str,
    email: Optional[str] = None,
    days: int = 7 * 4,  # 4 weeks
) -> None:
    """Show upcoming on-call shifts for a user.

    Args:
        session: PagerDuty API session
        schedule_id: PagerDuty schedule ID
        email: Optional email address to look up user ID
        days: Number of days to look ahead (default: 28 days / 4 weeks)
    """
    if not email:
        print("Email address is required", file=sys.stderr)
        sys.exit(1)

    user_id = get_user_id_by_email(session, email)
    until = datetime.now(tz.tzlocal()) + timedelta(days=days)

    shifts = get_unique_shifts(session, user_id, schedule_id, until)
    if not shifts:
        print("No upcoming shifts found")
        return

    print(f"Upcoming shifts for the next {days} days:")
    for start, end in shifts:
        print(f"{start.strftime('%Y-%m-%d %H:%M %Z')} to {end.strftime('%Y-%m-%d %H:%M %Z')}")
