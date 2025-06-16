"""Data models for the myshift package."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """Represents a PagerDuty user."""

    id: str
    name: str
    email: str
    time_zone: str
    role: Optional[str] = None


@dataclass
class Shift:
    """Represents a single shift in a schedule."""

    start: datetime
    end: datetime
    user: User
    schedule_id: str
    layer_id: Optional[str] = None


@dataclass
class Schedule:
    """Represents a PagerDuty schedule."""

    id: str
    name: str
    description: Optional[str] = None
    time_zone: Optional[str] = None
    layers: Optional[list] = None
    final_schedule: Optional[list[Shift]] = None
    override_schedule: Optional[list[Shift]] = None 