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

import argparse
import sys
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from myshift.config import load_config
from myshift.util import (
    get_pd_session,
    resolve_schedule_id,
    get_user_id_by_email,
    get_user_name_by_id,
    get_unique_shifts,
)

MAX_MONTHS_AHEAD = 3


def next_main(args: Optional[List[str]] = None, config: Optional[Dict[str, Any]] = None) -> None:
    """Main entry point for the next command.

    This function handles the next sub-command, allowing users to:
    1. View the next upcoming shift for a specific user
    2. Look ahead up to 3 months for the next shift
    3. Identify users by ID or email

    Command-line arguments:
        schedule_id: Optional PagerDuty schedule ID to check
        --user-id: Optional user ID to check (overrides my_user from config)
        --user-email: Optional user email to check (overrides my_user from config)

    Args:
        args: Optional command line arguments
        config: Optional configuration dictionary

    Raises:
        SystemExit: If required arguments are missing or if API calls fail
    """
    parser = argparse.ArgumentParser(description="Show the next on-call shift for a user.")
    parser.add_argument("schedule_id", nargs="?", help="PagerDuty schedule ID to check")
    group = parser.add_mutually_exclusive_group(
        required=False
    )  # Changed to not required since we can use config
    group.add_argument(
        "--user-id", help="PagerDuty user ID to check (overrides my_user from config)"
    )
    group.add_argument(
        "--user-email", help="PagerDuty user email to check (overrides my_user from config)"
    )
    parsed_args = parser.parse_args(args)

    if config is None:
        config = load_config()

    # Check if we have a user specified either via args or config
    if not (parsed_args.user_id or parsed_args.user_email or config.get("my_user")):
        print(
            "No user specified. Either use --user-id/--user-email or set my_user in config.",
            file=sys.stderr,
        )
        sys.exit(2)

    schedule_id = resolve_schedule_id(parsed_args, config)
    session = get_pd_session(config)

    if parsed_args.user_id:
        user_id = parsed_args.user_id
    elif parsed_args.user_email:
        user_id = get_user_id_by_email(session, parsed_args.user_email)
    else:
        # Use my_user from config
        my_user = config.get("my_user")
        if "@" in my_user:
            user_id = get_user_id_by_email(session, my_user)
        else:
            user_id = my_user

    user_name = get_user_name_by_id(session, user_id)
    now = datetime.now(timezone.utc)
    end_date = now + relativedelta(months=+MAX_MONTHS_AHEAD)
    unique_shifts = get_unique_shifts(session, user_id, schedule_id, end_date)

    if not unique_shifts:
        print(
            f"No upcoming shifts found for {user_name} ({user_id}) in the next {MAX_MONTHS_AHEAD} months."
        )
        return

    # The first shift in the sorted list is the next one
    start, end = unique_shifts[0]
    print(f"Next on-call shift for {user_name} ({user_id}):")
    day = start.strftime("%Y-%m-%d")
    start_str = start.strftime("%H:%M")
    end_str = end.strftime("%H:%M")
    print(f"  {day}: {start_str} to {end_str}")
