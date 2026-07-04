"""Momentum Features (ROC, RSI)."""

from collections import deque
from typing import Any, Dict, List
from Shared.models.market import MarketSnapshot
from Backend.features.base import AbstractFeature


class ROCFeature(AbstractFeature):
    """Rate of Change over a specified lookback period."""

    def __init__(self, lookback: int = 5) -> None:
        self.lookback = lookback
        self._history = deque(maxlen=self.lookback + 1)  # type: ignore

    @classmethod
    def get_name(cls) -> str:
        return "ROC_5"

    @classmethod
    def get_version(cls) -> str:
        return "v1"

    @classmethod
    def get_dependencies(cls) -> List[str]:
        return []

    @classmethod
    def warmup_period(cls) -> int:
        return 5

    def compute(self, snapshot: MarketSnapshot, dependency_values: Dict[str, Any]) -> Any:
        price = float(snapshot.close)
        self._history.append(price)
        
        if len(self._history) < self.lookback + 1:
            return None
            
        old_price = self._history[0]
        if old_price == 0:
            return 0.0
            
        return (price - old_price) / old_price


class RSIFeature(AbstractFeature):
    """
    Computes the Relative Strength Index (RSI) using Wilder's Smoothing.
    """

    def __init__(self, period: int = 14) -> None:
        self.period = period
        self._gains = deque()  # type: ignore
        self._losses = deque()  # type: ignore
        self._avg_gain = None
        self._avg_loss = None
        self._prev_price = None
        self._bar_count = 0

    @classmethod
    def get_name(cls) -> str:
        return "RSI_14"

    @classmethod
    def get_version(cls) -> str:
        return "v1"

    @classmethod
    def get_dependencies(cls) -> List[str]:
        return []

    @classmethod
    def warmup_period(cls) -> int:
        return 14

    def compute(self, snapshot: MarketSnapshot, dependency_values: Dict[str, Any]) -> Any:
        price = float(snapshot.close)
        
        if self._prev_price is None:
            self._prev_price = price  # type: ignore
            self._bar_count += 1
            return None

        change = price - self._prev_price
        self._prev_price = price
        self._bar_count += 1

        gain = change if change > 0 else 0.0
        loss = -change if change < 0 else 0.0

        if self._bar_count <= self.period + 1:
            self._gains.append(gain)
            self._losses.append(loss)

            if self._bar_count == self.period + 1:
                # Initialize smoothing with SMA
                self._avg_gain = sum(self._gains) / self.period
                self._avg_loss = sum(self._losses) / self.period
                self._gains.clear()
                self._losses.clear()
                return self._calculate_rsi()
            return None

        # Wilder's Smoothing
        self._avg_gain = (self._avg_gain * (self.period - 1) + gain) / self.period
        self._avg_loss = (self._avg_loss * (self.period - 1) + loss) / self.period

        return self._calculate_rsi()

    def _calculate_rsi(self) -> float:
        if self._avg_loss == 0:
            if self._avg_gain == 0:
                return 50.0
            return 100.0
        rs = self._avg_gain / self._avg_loss  # type: ignore
        return 100.0 - (100.0 / (1.0 + rs))  # type: ignore
