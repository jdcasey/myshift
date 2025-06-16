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

"""Main entry point for the myshift command-line tool.

This module provides the command-line interface for myshift, handling:
- Command-line argument parsing
- Sub-command routing
- Help text generation

Available sub-commands:
- override: Override PagerDuty schedule rotations
- upcoming: Show upcoming on-call shifts
- plan: Show all on-call shifts
- next: Show next on-call shift
- repl: Start interactive REPL
"""

import argparse
import sys
from typing import Optional, List, Any
from myshift.override import override_main
from myshift.upcoming import upcoming_main
from myshift.plan import plan_main
from myshift.repl import repl_main
from myshift.next import next_main

def main() -> None:
    """Main entry point for the myshift CLI tool.
    
    This function:
    1. Parses command-line arguments
    2. Routes to appropriate sub-command handler
    3. Handles help text generation
    
    Sub-commands:
        override: Override PagerDuty schedule rotations
        upcoming: Show upcoming on-call shifts for a user
        plan: Show all on-call shifts for the coming N weeks
        next: Show the next on-call shift for a user
        repl: Start an interactive REPL for myshift commands
    
    Raises:
        SystemExit: If invalid command is provided
    """
    parser = argparse.ArgumentParser(description='MyShift CLI tool')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Add the override sub-command
    override_parser = subparsers.add_parser('override', help='Override PagerDuty schedule rotations')
    # Add the upcoming sub-command
    upcoming_parser = subparsers.add_parser('upcoming', help='Show upcoming on-call shifts for a user')
    # Add the plan sub-command
    plan_parser = subparsers.add_parser('plan', help='Show all on-call shifts for the coming N weeks')
    # Add the next sub-command
    next_parser = subparsers.add_parser('next', help='Show the next on-call shift for a user')
    # Add the repl sub-command
    repl_parser = subparsers.add_parser('repl', help='Start an interactive REPL for myshift commands')

    args, extra_args = parser.parse_known_args()

    if args.command == 'override':
        override_main(extra_args)
    elif args.command == 'upcoming':
        upcoming_main(extra_args)
    elif args.command == 'plan':
        plan_main(extra_args)
    elif args.command == 'next':
        next_main(extra_args)
    elif args.command == 'repl':
        repl_main(extra_args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main() 