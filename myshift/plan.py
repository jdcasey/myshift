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

"""Schedule planning for PagerDuty on-call schedules.

This module provides functionality to view and plan on-call schedules,
including:
- Viewing all shifts in a schedule for a specified time period
- Displaying shifts with user information
- Configurable look-ahead period
"""

import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from dateutil import tz
from pagerduty import RestApiV2Client

from myshift.util import UserObject, build_user_map, get_all_unique_shifts


def plan_shifts(
    session: RestApiV2Client,
    schedule_id: str,
    days: int = 28,  # 4 weeks
) -> None:
    """Show planned shifts for a period.

    Args:
        session: PagerDuty API session
        schedule_id: PagerDuty schedule ID
        days: Number of days to show (default: 28 days / 4 weeks)

    Raises:
        SystemExit: If API calls fail
    """
    try:
        until = datetime.now(tz.tzlocal()) + timedelta(days=days)
        shifts = get_all_unique_shifts(session, schedule_id, until)
        user_map = build_user_map(session, shifts)

        if not shifts:
            print("No shifts found")
            return

        print(f"Shifts for the next {days} days:")
        for start, end, user_id in shifts:
            user = user_map.get(user_id, {"name": "Unknown"})
            print(f"{start.strftime('%Y-%m-%d %H:%M %Z')} to " f"{end.strftime('%Y-%m-%d %H:%M %Z')}: {user['name']}")
    except Exception as e:
        print(f"Error planning shifts: {e}", file=sys.stderr)
        sys.exit(1)
