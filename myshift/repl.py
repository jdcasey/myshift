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

import argparse
import sys
import shlex
import cmd
from typing import Optional, List, Any, Dict
from myshift.override import override_main
from myshift.upcoming import upcoming_main
from myshift.plan import plan_main
from myshift.next import next_main
from myshift.config import load_config, config_main

class MyShiftREPL(cmd.Cmd):
    intro = """Welcome to the myshift REPL. Type 'help' or '?' to list commands.
Type 'help <command>' for detailed help on a specific command.
Type 'exit', 'quit', or press Ctrl+D to exit."""
    prompt = '(myshift) '

    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config

    def do_override(self, arg: str) -> None:
        """Override PagerDuty schedule rotations."""
        try:
            override_main(shlex.split(arg), self.config)
        except SystemExit:
            pass

    def do_upcoming(self, arg: str) -> None:
        """Show upcoming on-call shifts for a user."""
        try:
            upcoming_main(shlex.split(arg), self.config)
        except SystemExit:
            pass

    def do_plan(self, arg: str) -> None:
        """Show all on-call shifts for the coming N weeks."""
        try:
            plan_main(shlex.split(arg), self.config)
        except SystemExit:
            pass

    def do_next(self, arg: str) -> None:
        """Show the next on-call shift."""
        try:
            next_main(shlex.split(arg), self.config)
        except SystemExit:
            pass

    def do_config(self, arg: str) -> None:
        """Validate or print sampleconfiguration."""
        config_main(arg.split() if arg else None)

    def do_exit(self, arg: str) -> bool:
        "Exit the REPL."
        print("Exiting myshift REPL.")
        return True

    def do_quit(self, arg: str) -> bool:
        "Exit the REPL."
        return self.do_exit(arg)

    def do_EOF(self, arg: str) -> bool:
        "Handle Ctrl+D (EOF) gracefully."
        print("\nExiting myshift REPL.")
        return True

    def emptyline(self) -> None:
        pass

    def default(self, line: str) -> None:
        print(f"Unknown command: {line}")
        print("Type 'help' for a list of available commands.")


def repl_main(args: Optional[List[str]] = None) -> None:
    print("Type 'help' for a list of commands. Arguments are the same as the CLI sub-commands.")
    try:
        config = load_config()
        MyShiftREPL(config).cmdloop()
    except KeyboardInterrupt:
        print("\nExiting myshift REPL.")
        sys.exit(0) 