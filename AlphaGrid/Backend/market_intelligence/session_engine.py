"""
Session Engine.

Evaluates trading sessions, pre-open logic, and kill zones.
Enforces the logic for intraday boundaries and session exclusions.

Dependency Graph:
    Consumes: [ExchangeContract]
    Produces: [Session State]
    Registry: MarketIntelligenceRegistry (Future)
    Downstream: MarketStateEngine, NormalizationEngine
    Owner: MarketIntelligenceTeam
"""

from datetime import datetime, time
from typing import Any

# Import MarketState from market_state_engine (delayed import/string reference to avoid circular imports in some structures, 
# but for now we import directly since market_state_engine imports this module ideally via dependency injection).
from Backend.market_intelligence.market_state_engine import MarketState


class SessionEngine:
    """Manages intraday market sessions and kill zones."""

    def __init__(self, exchange_contract: Any = None):
        """
        Initializes the Session Engine.
        
        Args:
            exchange_contract: The contract defining standard hours for the exchange.
        """
        self._exchange = exchange_contract

    def get_session_state(self, timestamp: datetime, exchange_code: str = "NSE") -> MarketState:
        """
        Determines the intraday session state.
        
        Args:
            timestamp (datetime): The time to evaluate.
            exchange_code (str): The exchange to check against.
            
        Returns:
            MarketState: The state (OPEN, PREOPEN, POSTMARKET, CLOSED).
        """
        if not self._exchange or self._exchange.exchange_code != exchange_code:
            return MarketState.CLOSED

        hours = self._exchange.get_standard_market_hours()
        current_time = timestamp.time()

        if hours["pre_open_start"] <= current_time < hours["pre_open_end"]:
            return MarketState.PREOPEN
            
        if hours["open"] <= current_time < hours["close"]:
            return MarketState.OPEN
            
        if hours["close"] <= current_time < hours["post_close_end"]:
            return MarketState.POSTMARKET
            
        return MarketState.CLOSED

    def is_kill_zone(self, timestamp: datetime, exchange_code: str = "NSE") -> bool:
        """
        Determines if the given time is within a defined 'kill zone'
        (periods of low liquidity or high volatility where trading is restricted).
        
        Args:
            timestamp (datetime): The time to evaluate.
            exchange_code (str): The exchange.
            
        Returns:
            bool: True if in a kill zone, False otherwise.
        """
        # For NSE, a common kill zone might be the first 15 mins of open
        # or the last 30 mins before close. This should ideally be configurable.
        if not self._exchange or self._exchange.exchange_code != exchange_code:
            return True # If closed/unknown, it's essentially a kill zone

        current_time = timestamp.time()
        
        # Hardcoded example, should be moved to configuration
        first_15_mins_end = time(9, 30)
        last_30_mins_start = time(15, 0)
        
        hours = self._exchange.get_standard_market_hours()
        
        if hours["open"] <= current_time < first_15_mins_end:
            return True
            
        if last_30_mins_start <= current_time < hours["close"]:
            return True
            
        return False

    def calculate_expected_bars(self, start_time: datetime, end_time: datetime, timeframe: str) -> int:
        """
        Calculates the mathematically expected number of bars between two timestamps.
        
        (ADR-003): The SessionEngine owns this logic to account for market hours,
        weekends, and holidays.
        """
        import numpy as np
        
        # Determine total days (ignoring holidays for the naive phase)
        start_date = start_time.date()
        end_date = end_time.date()
        
        # Crypto vs Traditional markets - we assume 24/7 if not NSE for this slice
        if not self._exchange or self._exchange.exchange_code != "NSE":
            # Assume 24/7 crypto for the synthetic dataset
            total_days = (end_date - start_date).days + 1
            minutes_per_day = 1440
        else:
            # Traditional business days
            total_days = int(np.busday_count(start_date, end_date))
            if start_date <= end_date and np.is_busday(end_date):
                total_days += 1
            minutes_per_day = 375 # 6h 15m for NSE
            
        if timeframe.endswith('m'):
            tf_minutes = int(timeframe[:-1])
            bars_per_day = minutes_per_day // tf_minutes
        elif timeframe.endswith('h') or timeframe.endswith('H'):
            tf_hours = int(timeframe[:-1])
            bars_per_day = minutes_per_day // (tf_hours * 60)
            if bars_per_day == 0:
                bars_per_day = 1
        elif timeframe.endswith('d') or timeframe.endswith('D'):
            bars_per_day = 1
        else:
            bars_per_day = 1
            
        return max(1, total_days * bars_per_day)

