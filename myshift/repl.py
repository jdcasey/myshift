"""Interactive REPL (Read-Eval-Print Loop) for myshift commands.

This module provides an interactive command-line interface for myshift,
allowing users to execute myshift commands without having to type the
'myshift' prefix each time. It supports all main myshift commands and
provides help text and command history.
"""

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
    """Interactive REPL for myshift commands.

    This class provides a command-line interface that supports:
    - Command history (up/down arrows)
    - Tab completion
    - Help text for all commands
    - Graceful exit handling

    All myshift commands are available as sub-commands, with the same
    arguments as their CLI counterparts.
    """

    intro = """Welcome to the myshift REPL. Type 'help' or '?' to list commands.
Type 'help <command>' for detailed help on a specific command.
Type 'exit', 'quit', or press Ctrl+D to exit."""
    prompt = "(myshift) "

    def __init__(self, config: Dict[str, Any]):
        """Initialize the REPL with configuration.

        Args:
            config: Configuration dictionary for myshift
        """
        super().__init__()
        self.config = config

    def do_help(self, arg: str) -> None:
        """Show help for commands.

        Args:
            arg: Optional command name to show help for
        """
        if arg:
            # Show help for specific command
            super().do_help(arg)
        else:
            # Show list of all commands
            print("\nAvailable commands:")
            print("-----------------")
            print("next      - Show your next on-call shift")
            print("upcoming  - Show your upcoming on-call shifts")
            print("plan      - Show the entire on-call schedule")
            print("override  - Override a shift in the schedule")
            print("config    - View or modify configuration")
            print("help      - Show this help message")
            print("exit      - Exit the REPL")
            print("\nType 'help <command>' for detailed help on a specific command.")

    def do_override(self, arg: str) -> None:
        """Override PagerDuty schedule rotations.

        Usage: override [schedule_id] [options]

        Options:
            --start-date YYYY-MM-DD    Start date for override
            --end-date YYYY-MM-DD      End date for override
            --user-id ID               User ID to assign
            --user-email EMAIL         User email to assign
            --target-user-id ID        Target user ID to override
            --target-user-email EMAIL  Target user email to override
            --dry-run                  Show what would be overridden
        """
        try:
            override_main(shlex.split(arg), self.config)
        except SystemExit:
            pass

    def do_upcoming(self, arg: str) -> None:
        """Show upcoming on-call shifts for a user.

        Usage: upcoming [schedule_id] [options]

        Options:
            --user-id ID       User ID to check
            --user-email EMAIL User email to check
            --weeks N         Number of weeks to look ahead (default: 4)
        """
        try:
            upcoming_main(shlex.split(arg), self.config)
        except SystemExit:
            pass

    def do_plan(self, arg: str) -> None:
        """Show all on-call shifts for the coming N weeks.

        Usage: plan [schedule_id] [options]

        Options:
            --weeks N    Number of weeks to look ahead (default: 4)
        """
        try:
            plan_main(shlex.split(arg), self.config)
        except SystemExit:
            pass

    def do_next(self, arg: str) -> None:
        """Show the next on-call shift.

        Usage: next [schedule_id] [options]

        Options:
            --user-id ID       User ID to check
            --user-email EMAIL User email to check
        """
        try:
            next_main(shlex.split(arg), self.config)
        except SystemExit:
            pass

    def do_config(self, arg: str) -> None:
        """Validate or print sample configuration.

        Usage: config [options]

        Options:
            --print    Print sample configuration
        """
        config_main(arg.split() if arg else None)

    def do_exit(self, arg: str) -> bool:
        """Exit the REPL.

        Returns:
            True to exit the REPL
        """
        print("Exiting myshift REPL.")
        return True

    def do_quit(self, arg: str) -> bool:
        """Exit the REPL (alias for exit).

        Returns:
            True to exit the REPL
        """
        return self.do_exit(arg)

    def do_EOF(self, arg: str) -> bool:
        """Handle Ctrl+D (EOF) gracefully.

        Returns:
            True to exit the REPL
        """
        print("\nExiting myshift REPL.")
        return True

    def emptyline(self) -> None:
        """Handle empty line input."""
        pass

    def default(self, line: str) -> None:
        """Handle unknown commands.

        Args:
            line: The unknown command line
        """
        print(f"Unknown command: {line}")
        print("Type 'help' for a list of available commands.")


def repl_main(args: Optional[List[str]] = None) -> None:
    """Start the interactive REPL.

    Args:
        args: Optional command line arguments (unused)

    Raises:
        SystemExit: On keyboard interrupt
    """
    print("Type 'help' for a list of commands. Arguments are the same as the CLI sub-commands.")
    try:
        config = load_config()
        MyShiftREPL(config).cmdloop()
    except KeyboardInterrupt:
        print("\nExiting myshift REPL.")
        sys.exit(0)
