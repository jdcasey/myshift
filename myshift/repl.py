"""Interactive REPL for MyShift commands."""

import cmd
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from dateutil import tz
from pagerduty import RestApiV2Client

from myshift.next import next_shift
from myshift.override import create_override
from myshift.plan import plan_shifts
from myshift.util import get_user_id_by_email


class MyShiftShell(cmd.Cmd):
    """Interactive shell for MyShift commands."""

    intro = "Welcome to MyShift REPL. Type help or ? to list commands.\n"
    prompt = "(myshift) "

    def __init__(self, session: RestApiV2Client, schedule_id: str):
        """Initialize the shell.

        Args:
            session: PagerDuty API session
            schedule_id: PagerDuty schedule ID
        """
        super().__init__()
        self.session = session
        self.schedule_id = schedule_id

    def do_next(self, arg: str) -> None:
        """Show the next on-call shift.

        Usage: next [email]
        """
        if not arg:
            print("Email address is required", file=sys.stderr)
            return

        try:
            next_shift(self.session, self.schedule_id, arg)
        except Exception as e:
            print(f"Error showing next shift: {e}", file=sys.stderr)

    def do_plan(self, arg: str) -> None:
        """Show planned shifts for a period.

        Usage: plan [days]
        """
        try:
            days = int(arg) if arg else 7
        except ValueError:
            print("Days must be a number", file=sys.stderr)
            return

        try:
            plan_shifts(self.session, self.schedule_id, days)
        except Exception as e:
            print(f"Error showing planned shifts: {e}", file=sys.stderr)

    def do_override(self, arg: str) -> None:
        """Create an override for a shift.

        Usage: override <user-email> <target-email> <start> [end]
        Example: override user@example.com target@example.com 2024-03-20 [2024-03-21]
        """
        try:
            parts = arg.split()
            if len(parts) < 3:
                raise ValueError
            user_email = parts[0]
            target_email = parts[1]
            start = parts[2]
            end = parts[3] if len(parts) > 3 else None
        except ValueError:
            print(
                "Usage: override <user-email> <target-email> <start> [end]",
                file=sys.stderr,
            )
            return

        try:
            create_override(
                self.session,
                self.schedule_id,
                user_email=user_email,
                target_user_email=target_email,
                start_str=start,
                end_str=end,
            )
        except Exception as e:
            print(f"Error creating override: {e}", file=sys.stderr)

    def do_quit(self, arg: str) -> bool:
        """Exit the REPL."""
        print("Goodbye!")
        return True

    def do_EOF(self, arg: str) -> bool:
        """Exit the REPL on EOF."""
        print()
        return self.do_quit(arg)


def start_repl(session: RestApiV2Client, schedule_id: str) -> None:
    """Start the interactive REPL.

    Args:
        session: PagerDuty API session
        schedule_id: PagerDuty schedule ID

    Raises:
        SystemExit: If the REPL encounters an unrecoverable error
    """
    try:
        shell = MyShiftShell(session, schedule_id)
        shell.cmdloop()
    except Exception as e:
        print(f"Error starting REPL: {e}", file=sys.stderr)
        sys.exit(1)
