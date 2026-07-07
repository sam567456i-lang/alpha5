from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class FreshnessProfileDTO:
    created_at: datetime
    updated_at: datetime
    expires_at: datetime
    is_stale: bool
    refresh_count: int
