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

import argparse
import sys
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone, timedelta
from dateutil import tz
from myshift.config import load_config
from myshift.util import get_pd_session, resolve_schedule_id, get_all_unique_shifts, build_user_map
import yaml


def plan_main(args: Optional[List[str]] = None, config: Optional[Dict[str, Any]] = None) -> None:
    """Main entry point for the plan command.

    This function handles the plan sub-command, allowing users to:
    1. View all shifts in a schedule for a specified time period
    2. See which users are on call during each shift
    3. Configure the look-ahead period

    Command-line arguments:
        schedule_id: Optional PagerDuty schedule ID to check
        --weeks: Optional number of weeks to look ahead (default: 4)

    Args:
        args: Optional command line arguments
        config: Optional configuration dictionary

    Raises:
        SystemExit: If required arguments are missing or if API calls fail
    """
    parser = argparse.ArgumentParser(description="Show all on-call shifts for the coming N weeks.")
    parser.add_argument("schedule_id", nargs="?", help="PagerDuty schedule ID to check")
    parser.add_argument(
        "--weeks", type=int, default=4, help="Number of weeks to look ahead (default: 4)"
    )
    parser.add_argument(
        "--utc", action="store_true", help="Show times in UTC instead of local timezone"
    )
    parsed_args = parser.parse_args(args)

    if config is None:
        config = load_config()

    schedule_id = resolve_schedule_id(parsed_args, config)
    session = get_pd_session(config)

    now = datetime.now(timezone.utc)
    end_date = now + timedelta(weeks=parsed_args.weeks)
    target_tz = tz.tzutc() if parsed_args.utc else None
    unique_shifts = get_all_unique_shifts(session, schedule_id, end_date, target_tz)

    if not unique_shifts:
        print(f"No upcoming shifts found in the next {parsed_args.weeks} weeks.")
        return

    # Build a map of user objects for display
    user_map = build_user_map(session, unique_shifts)

    # Print shifts
    print(f"\nOn-call schedule for the next {parsed_args.weeks} weeks:")
    for start, end, user_id in unique_shifts:
        day = start.strftime("%Y-%m-%d")
        start_str = start.strftime("%H:%M")
        end_str = end.strftime("%H:%M")

        user = user_map.get(user_id, {})
        user_name = user.get("name", "Unknown")
        user_email = user.get("email", "Unknown")
        print(f"{day}: {start_str} to {end_str}:\n\t{user_name} ({user_email})")
