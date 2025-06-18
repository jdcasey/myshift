"""MyShift - A command-line tool for managing PagerDuty on-call schedules.

Features:
- View upcoming shifts
- Plan future schedules
- Override shifts
- Interactive REPL mode
"""

from typing import Final

__version__: Final = "0.1.0"

from myshift.config import load_config
from myshift.util import (
    build_user_map,
    get_all_unique_shifts,
    get_pd_session,
    get_unique_shifts,
    get_user_id_by_email,
    get_user_name_by_id,
    resolve_schedule_id,
)
