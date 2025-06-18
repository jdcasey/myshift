"""Create an override for a PagerDuty schedule."""

import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, TypedDict

from dateutil import parser as date_parser
from dateutil import tz
from pagerduty import RestApiV2Client, HttpError, UrlError

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
            "schedule_ids": [schedule_id],  # Use modern list format
            "since": start_date.isoformat(),
            "until": end_date.isoformat(),
            "user_ids": [target_user_id],  # More efficient filtering
        }
        
        # Use modern iter_all for automatic pagination
        all_oncalls = list(session.iter_all("/oncalls", params=params))
        
        for oc in all_oncalls:
            if oc.get("user", {}).get("id") == target_user_id:
                shifts.append({"start": oc["start"], "end": oc["end"]})
                
        return shifts
        
    except HttpError as e:
        print(f"PagerDuty API error fetching shifts: {e.response.status_code} - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error fetching shifts: {e}", file=sys.stderr)
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

    # Use context manager for better resource management
    try:
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
                f"No consecutive shifts found for user {target_user_id} "
                f"starting from {start_str}",
                file=sys.stderr,
            )
            sys.exit(1)

        # Create overrides using modern batch creation pattern
        # The API supports creating multiple overrides in one request
        overrides_to_create = [
            {
                "start": shift["start"],
                "end": shift["end"],
                "user": {"id": user_id, "type": "user_reference"},
                "time_zone": "UTC"  # Explicitly set timezone
            }
            for shift in shifts
        ]

        # Use modern rpost for wrapped entity handling
        try:
            result = session.rpost(
                f"/schedules/{schedule_id}/overrides", 
                json=overrides_to_create  # Modern pattern: pass list directly
            )
            
            if result:
                user_name = get_user_name_by_id(session, user_id)
                print(f"Successfully created {len(shifts)} override(s) for {user_name}")
                for i, shift in enumerate(shifts, 1):
                    print(f"Override {i}:")
                    print(f"  Start: {shift['start']}")
                    print(f"  End: {shift['end']}")
            else:
                print("Failed to create override", file=sys.stderr)
                sys.exit(1)
                
        except HttpError as e:
            if e.response.status_code == 400:
                print(f"Invalid override request: {e}", file=sys.stderr)
                # Try to extract specific error details from response
                try:
                    error_details = e.response.json()
                    if "errors" in error_details:
                        for error in error_details["errors"]:
                            print(f"  - {error}", file=sys.stderr)
                except:
                    pass
            elif e.response.status_code == 403:
                print("Insufficient permissions to create overrides", file=sys.stderr)
            elif e.response.status_code == 404:
                print(f"Schedule {schedule_id} not found", file=sys.stderr)
            else:
                print(f"PagerDuty API error: {e.response.status_code} - {e}", file=sys.stderr)
            sys.exit(1)
            
    except UrlError as e:
        print(f"Invalid API request: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error creating override: {e}", file=sys.stderr)
        sys.exit(1)
