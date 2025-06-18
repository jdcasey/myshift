"""Create an override for a PagerDuty schedule."""

import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, TypedDict

from dateutil import parser as date_parser
from dateutil import tz
from pagerduty import RestApiV2Client

from myshift.util import get_user_id_by_email, get_user_name_by_id


class ShiftDict(TypedDict):
    """Type definition for shift dictionaries."""

    start: str
    end: str


def get_consecutive_target_shifts(
    session: RestApiV2Client,
    schedule_id: str,
    target_user_id: str,
    start_date: datetime,
    end_date: Optional[datetime] = None,
) -> List[ShiftDict]:
    """Get consecutive shifts for a target user starting from a specific date.

    Args:
        session: PagerDuty API session
        schedule_id: PagerDuty schedule ID
        target_user_id: User ID whose shifts to get
        start_date: Date to start looking for shifts
        end_date: Optional end date to limit shifts (defaults to 14 days from start)

    Returns:
        List of shift dictionaries with start and end times

    Raises:
        SystemExit: If API calls fail
    """
    try:
        shifts: List[ShiftDict] = []
        if end_date is None:
            end_date = start_date + timedelta(days=14)
        params = {
            "schedule_ids[]": schedule_id,
            "since": start_date.isoformat(),
            "until": end_date.isoformat(),
        }
        resp = session.rget("/oncalls", params=params)
        for oc in resp["oncalls"]:
            if oc.get("user", {}).get("id") == target_user_id:
                shifts.append({"start": oc["start"], "end": oc["end"]})
                break
        return shifts
    except Exception as e:
        print(f"Error fetching shifts: {e}", file=sys.stderr)
        sys.exit(1)


def create_override(
    session: RestApiV2Client,
    schedule_id: str,
    user_id: Optional[str] = None,
    user_email: Optional[str] = None,
    target_user_id: Optional[str] = None,
    target_user_email: Optional[str] = None,
    start_str: Optional[str] = None,
    end_str: Optional[str] = None,
) -> None:
    """Create an override for a PagerDuty schedule.

    Args:
        session: PagerDuty API session
        schedule_id: PagerDuty schedule ID
        user_id: PagerDuty user ID to override with
        user_email: PagerDuty user email to override with
        target_user_id: PagerDuty user ID whose shifts will be overridden
        target_user_email: PagerDuty user email whose shifts will be overridden
        start_str: Start date string (YYYY-MM-DD)
        end_str: Optional end date string (YYYY-MM-DD) to limit overrides

    Raises:
        SystemExit: If required parameters are missing or API calls fail
    """
    if not user_id and not user_email:
        print("User ID or email is required", file=sys.stderr)
        sys.exit(1)

    if not target_user_id and not target_user_email:
        print("Target user ID or email is required", file=sys.stderr)
        sys.exit(1)

    if not start_str:
        print("Start date is required (format: YYYY-MM-DD)", file=sys.stderr)
        sys.exit(1)

    try:
        start = datetime.strptime(start_str, "%Y-%m-%d")
        end = datetime.strptime(end_str, "%Y-%m-%d") + timedelta(days=1) if end_str else None
    except ValueError as e:
        print(f"Invalid date format: {e}. Use YYYY-MM-DD.", file=sys.stderr)
        sys.exit(1)

    # Determine user_id if email provided
    if not user_id:
        user_id = get_user_id_by_email(session, user_email)

    # Determine target_user_id
    if not target_user_id:
        target_user_id = get_user_id_by_email(session, target_user_email)

    # Get consecutive shifts for the target user
    shifts = get_consecutive_target_shifts(session, schedule_id, target_user_id, start, end)
    if not shifts:
        print(
            f"No consecutive shifts found for user {target_user_id} " f"starting from {start_str}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Create an override for each shift
    override_data = {
        "override": [
            {
                "start": shift["start"],
                "end": shift["end"],
                "user": {"id": user_id, "type": "user_reference"},
            }
            for shift in shifts
        ]
    }

    try:
        result = session.rpost(f"/schedules/{schedule_id}/overrides", override_data)
        if result:
            user_name = get_user_name_by_id(session, user_id)
            print(f"Created override for {user_name}")
            for shift in shifts:
                print(f"Start: {shift['start']}")
                print(f"End: {shift['end']}")
        else:
            print("Failed to create override", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error creating override: {e}", file=sys.stderr)
        sys.exit(1)
