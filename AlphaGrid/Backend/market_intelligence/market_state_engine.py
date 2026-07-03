"""
Market State Engine.

Purpose
-------
Single authoritative source for Market State. Instead of duplicating
session/holiday/circuit checks across modules, everything queries this service.

Consumes
--------
SessionEngine
TradingCalendar
LiveDataProvider

Produces
--------
MarketState

Registry
--------
MarketIntelligenceRegistry

Downstream
----------
OpportunityScanner
FeatureEngine

Inputs
------
timestamp (datetime), exchange (str)

Outputs
-------
MarketState (Enum)

Failure Modes
-------------
Missing Calendar -> Fallback to CLOSED
Missing Session -> Fallback to CLOSED

Complexity
----------
Time: O(1)
Space: O(1)

Thread Safety
-------------
Yes - Stateless queries with atomic overrides.

Determinism
-----------
Deterministic based on current calendar state.

Version
-------
1.0.0

Tests
-----
tests/market_intelligence/test_market_state.py
"""

from enum import Enum
from datetime import datetime
from typing import Optional, Any

class MarketState(Enum):
    OPEN = "OPEN"
    PREOPEN = "PREOPEN"
    POSTMARKET = "POSTMARKET"
    HOLIDAY = "HOLIDAY"
    EXPIRY = "EXPIRY"
    HALT = "HALT"
    CIRCUIT = "CIRCUIT"
    SPECIAL_SESSION = "SPECIAL_SESSION"
    CLOSED = "CLOSED"


class MarketStateEngine:
    """Authoritative source for real-time market state."""

    def __init__(self, session_engine: Any = None, trading_calendar: Any = None):
        """
        Initializes the Market State Engine.
        
        Args:
            session_engine: Engine that determines intraday sessions.
            trading_calendar: Engine that determines holidays and expiries.
        """
        self._session_engine = session_engine
        self._trading_calendar = trading_calendar
        self._manual_override_state: Optional[MarketState] = None

    def get_current_state(self, timestamp: datetime, exchange: str = "NSE") -> MarketState:
        """
        Determines the current market state for the given timestamp and exchange.
        
        Args:
            timestamp (datetime): The current time to evaluate.
            exchange (str): The exchange code.
            
        Returns:
            MarketState: The current state of the market.
        """
        if self._manual_override_state:
            return self._manual_override_state

        if self._trading_calendar and self._trading_calendar.is_holiday(timestamp, exchange):
            return MarketState.HOLIDAY

        if self._session_engine:
            return self._session_engine.get_session_state(timestamp, exchange)
            
        # Fallback if no engines are attached
        return MarketState.CLOSED

    def set_manual_override(self, state: Optional[MarketState]) -> None:
        """Allows manual override of the market state (e.g., for CIRCUIT breakers)."""
        self._manual_override_state = state
