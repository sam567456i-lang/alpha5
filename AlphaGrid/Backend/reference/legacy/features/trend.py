"""Trend Features (EMA, SMA, etc.)."""

from collections import deque
from typing import Any, Dict, List
from Shared.models.market import MarketSnapshot
from Backend.features.base import AbstractFeature


class SMAFeature(AbstractFeature):
    """
    Computes a Simple Moving Average (SMA) over a specified period.
    """

    def __init__(self, period: int = 20) -> None:
        self.period = period
        self._window = deque(maxlen=self.period)  # type: ignore

    @classmethod
    def get_name(cls) -> str:
        return "SMA_20"

    @classmethod
    def get_version(cls) -> str:
        return "v1"

    @classmethod
    def get_dependencies(cls) -> List[str]:
        return []

    @classmethod
    def warmup_period(cls) -> int:
        return 20

    def compute(self, snapshot: MarketSnapshot, dependency_values: Dict[str, Any]) -> Any:
        price = float(snapshot.close)
        self._window.append(price)

        if len(self._window) < self.period:
            return None

        return sum(self._window) / len(self._window)


class EMAFeature(AbstractFeature):
    """
    Computes an Exponential Moving Average (EMA).
    Properly initializes the EMA using an SMA over the warmup period.
    """

    def __init__(self, period: int = 20) -> None:
        self.period = period
        self.alpha = 2 / (self.period + 1)
        self._ema = None
        self._prices_buffer = []  # type: ignore
        self._initialized = False

    @classmethod
    def get_name(cls) -> str:
        return "EMA_20"

    @classmethod
    def get_version(cls) -> str:
        return "v1"

    @classmethod
    def get_dependencies(cls) -> List[str]:
        return []

    @classmethod
    def warmup_period(cls) -> int:
        return 20

    def compute(self, snapshot: MarketSnapshot, dependency_values: Dict[str, Any]) -> Any:
        price = float(snapshot.close)

        if not self._initialized:
            self._prices_buffer.append(price)
            if len(self._prices_buffer) == self.period:
                self._ema = sum(self._prices_buffer) / self.period
                self._initialized = True
            return None
        
        self._ema = (price - self._ema) * self.alpha + self._ema  # type: ignore
        return self._ema
