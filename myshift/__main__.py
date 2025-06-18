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

"""Command-line interface for MyShift."""

import argparse
import sys
from datetime import datetime, timedelta

import dateutil.parser as date_parser
import dateutil.tz

from myshift import __version__
from myshift.config import load_config
from myshift.next import next_shift
from myshift.override import create_override
from myshift.plan import plan_schedule
from myshift.repl import start_repl
from myshift.util import (
    get_pd_session,
    resolve_schedule_id,
)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Command-line interface for managing PagerDuty on-call schedules")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Next shift command
    next_parser = subparsers.add_parser("next", help="Show next shift")
    next_parser.add_argument("--user", help="Show next shift for specific user (email)")

    # Plan command
    plan_parser = subparsers.add_parser("plan", help="Plan future schedule")
    plan_parser.add_argument("--start", help="Start date (YYYY-MM-DD)", required=True)
    plan_parser.add_argument("--end", help="End date (YYYY-MM-DD)", required=True)

    # Override command
    override_parser = subparsers.add_parser("override", help="Create shift override")
    override_parser.add_argument("--user", help="User to override (email)", required=True)
    override_parser.add_argument("--start", help="Start time (YYYY-MM-DD HH:MM)", required=True)
    override_parser.add_argument("--end", help="End time (YYYY-MM-DD HH:MM)", required=True)

    # REPL command
    subparsers.add_parser("repl", help="Start interactive REPL")

    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()
    config = load_config()

    if args.command == "next":
        pd = get_pd_session(config)
        schedule_id = resolve_schedule_id(config)
        next_shift(pd, schedule_id, args.user)
        return 0

    if args.command == "plan":
        pd = get_pd_session(config)
        schedule_id = resolve_schedule_id(config)
        start = date_parser.parse(args.start)
        end = date_parser.parse(args.end)
        plan_schedule(pd, schedule_id, start, end)
        return 0

    if args.command == "override":
        pd = get_pd_session(config)
        schedule_id = resolve_schedule_id(config)
        start = date_parser.parse(args.start)
        end = date_parser.parse(args.end)
        create_override(pd, schedule_id, args.user, start, end)
        return 0

    if args.command == "repl":
        start_repl()
        return 0

    print("No command specified. Use --help for usage information.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
