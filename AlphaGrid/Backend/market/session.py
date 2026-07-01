"""Market Session Manager — handles market timings and holidays."""

from __future__ import annotations

import datetime
from zoneinfo import ZoneInfo


class MarketSessionManager:
    """Manages market session state (Open, Closed, Pre-Market)."""

    def __init__(self) -> None:
        self.tz = ZoneInfo("Asia/Kolkata")
        
        # In a full implementation, these would come from config or a database
        self.holidays = {
            datetime.date(2026, 1, 26),  # Republic Day
            datetime.date(2026, 3, 20),  # Holi (example)
            datetime.date(2026, 5, 1),   # Maharashtra Day
            datetime.date(2026, 8, 15),  # Independence Day
            datetime.date(2026, 10, 2),  # Gandhi Jayanti
            datetime.date(2026, 12, 25), # Christmas
        }

    def _now(self) -> datetime.datetime:
        """Return the current time in IST."""
        return datetime.datetime.now(self.tz)

    def is_holiday(self, date: datetime.date) -> bool:
        """Check if the given date is a market holiday."""
        if date.weekday() >= 5:  # Saturday=5, Sunday=6
            return True
        return date in self.holidays

    def current_session(self, exchange: str = "NSE") -> str:
        """Return the current market session state."""
        now = self._now()
        
        if self.is_holiday(now.date()):
            return "CLOSED"
            
        time_int = now.hour * 100 + now.minute
        
        if time_int < 900:
            return "CLOSED"
        elif 900 <= time_int < 915:
            return "PRE_OPEN"
        elif 915 <= time_int < 1530:
            return "OPEN"
        else:
            return "POST_CLOSE"

    def is_market_open(self, exchange: str = "NSE") -> bool:
        """Return True if the market is currently in the OPEN session."""
        return self.current_session(exchange) == "OPEN"
