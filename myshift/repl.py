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
from typing import Optional, List, Any
from myshift.override import override_main
from myshift.upcoming import upcoming_main
from myshift.plan import plan_main
from myshift.next import next_main

class MyShiftREPL(cmd.Cmd):
    intro = "Welcome to the myshift REPL. Type 'help' or '?' to list commands."
    prompt = '(myshift) '

    def do_override(self, arg: str) -> None:
        "Override PagerDuty schedule rotations. Usage: override [args...]"
        try:
            override_main(shlex.split(arg))
        except SystemExit:
            pass

    def do_upcoming(self, arg: str) -> None:
        "Show upcoming on-call shifts for a user. Usage: upcoming [args...]"
        try:
            upcoming_main(shlex.split(arg))
        except SystemExit:
            pass

    def do_plan(self, arg: str) -> None:
        "Show all on-call shifts for the coming N weeks. Usage: plan [args...]"
        try:
            plan_main(shlex.split(arg))
        except SystemExit:
            pass

    def do_exit(self, arg: str) -> bool:
        "Exit the REPL."
        print("Exiting myshift REPL.")
        return True

    def do_quit(self, arg: str) -> bool:
        "Exit the REPL."
        return self.do_exit(arg)

    def emptyline(self) -> None:
        pass

    def default(self, line: str) -> None:
        print(f"Unknown command: {line}")


def repl_main(args: Optional[List[str]] = None) -> None:
    print("Type 'help' for a list of commands. Arguments are the same as the CLI sub-commands.")
    MyShiftREPL().cmdloop() 