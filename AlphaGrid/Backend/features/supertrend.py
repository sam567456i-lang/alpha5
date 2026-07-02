"""SuperTrend Feature."""

from typing import Any, Dict, List
from Shared.models.market import MarketSnapshot
from Shared.enums.signal_direction import SignalDirection
from .base import AbstractFeature
from .protocols import TrendFeatureOutput

class SuperTrendFeature(AbstractFeature, TrendFeatureOutput):
    """
    Computes SuperTrend indicator based on ATR.
    O(n) streaming calculation.
    """

    def __init__(self, period: int = 10, multiplier: float = 3.0) -> None:
        self.period = period
        self.multiplier = multiplier
        self._prev_upper = 0.0
        self._prev_lower = 0.0
        self._prev_close = 0.0
        self._direction = SignalDirection.WAIT
        self._is_initialized = False
        
        # ATR state
        self._atr_tr_values = []  # type: ignore
        self._atr = None
        self._bar_count = 0

    @property
    def direction(self) -> SignalDirection:
        return self._direction

    @classmethod
    def get_name(cls) -> str:
        return "SuperTrend_10_3"

    @classmethod
    def get_version(cls) -> str:
        return "v2"

    @classmethod
    def get_dependencies(cls) -> List[str]:
        return []

    @classmethod
    def warmup_period(cls) -> int:
        return 10  # Waits for ATR to warm up

    def compute(self, snapshot: MarketSnapshot, dependency_values: Dict[str, Any]) -> Any:
        high = float(snapshot.high)
        low = float(snapshot.low)
        close = float(snapshot.close)
        
        # Calculate ATR internally
        if self._prev_close is None:
            tr = high - low
        else:
            tr = max(high - low, abs(high - self._prev_close), abs(low - self._prev_close))
            
        self._bar_count += 1
        
        if self._bar_count <= self.period:
            self._atr_tr_values.append(tr)
            if self._bar_count == self.period:
                self._atr = sum(self._atr_tr_values) / self.period
                self._atr_tr_values.clear()
            else:
                self._prev_close = close
                return None
        else:
            self._atr = (self._atr * (self.period - 1) + tr) / self.period  # type: ignore

        atr = self._atr
        
        basic_upper = ((high + low) / 2.0) + (self.multiplier * atr)  # type: ignore
        basic_lower = ((high + low) / 2.0) - (self.multiplier * atr)  # type: ignore

        if not self._is_initialized:
            self._prev_upper = basic_upper
            self._prev_lower = basic_lower
            self._prev_close = close
            self._direction = SignalDirection.LONG # Default start
            self._is_initialized = True
            return {"supertrend": basic_lower, "direction": self._direction, "upper": basic_upper, "lower": basic_lower}

        # Compute Upper Band
        if basic_upper < self._prev_upper or self._prev_close > self._prev_upper:
            upper = basic_upper
        else:
            upper = self._prev_upper

        # Compute Lower Band
        if basic_lower > self._prev_lower or self._prev_close < self._prev_lower:
            lower = basic_lower
        else:
            lower = self._prev_lower

        # Determine Trend Direction
        if self._direction == SignalDirection.LONG and close < lower:
            self._direction = SignalDirection.SHORT
        elif self._direction == SignalDirection.SHORT and close > upper:
            self._direction = SignalDirection.LONG

        self._prev_upper = upper
        self._prev_lower = lower
        self._prev_close = close
        
        val = lower if self._direction == SignalDirection.LONG else upper
        return {"supertrend": val, "direction": self._direction, "upper": upper, "lower": lower}
