"""Volatility Features (ATR, RelativeVolume)."""

from collections import deque
from typing import Any, Dict, List
from Shared.models.market import MarketSnapshot
from Backend.features.base import AbstractFeature


class ATRFeature(AbstractFeature):
    """
    Computes Average True Range (ATR) using Wilder's Smoothing.
    """

    def __init__(self, period: int = 14) -> None:
        self.period = period
        self._prev_close = None
        self._tr_values = deque()  # type: ignore
        self._atr = None
        self._bar_count = 0

    @classmethod
    def get_name(cls) -> str:
        return "ATR_14"

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
        high = float(snapshot.high)
        low = float(snapshot.low)
        close = float(snapshot.close)

        if self._prev_close is None:
            tr = high - low
        else:
            tr = max(high - low, abs(high - self._prev_close), abs(low - self._prev_close))
            
        self._prev_close = close  # type: ignore
        self._bar_count += 1

        if self._bar_count <= self.period:
            self._tr_values.append(tr)
            if self._bar_count == self.period:
                self._atr = sum(self._tr_values) / self.period
                self._tr_values.clear()
                return self._atr
            return None

        self._atr = (self._atr * (self.period - 1) + tr) / self.period  # type: ignore
        return self._atr


class RelativeVolumeFeature(AbstractFeature):
    """
    Computes Relative Volume (volume / SMA(volume)).
    """

    def __init__(self, period: int = 5) -> None:
        self.period = period
        self._volumes = deque(maxlen=self.period)  # type: ignore

    @classmethod
    def get_name(cls) -> str:
        return "RelativeVolume_5"

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
        volume = float(snapshot.volume)
        
        # Don't compute ratio against empty window
        if len(self._volumes) < self.period:
            self._volumes.append(volume)
            return None

        # Compute mean of PREVIOUS volumes
        mean_vol = sum(self._volumes) / self.period
        
        # Update window with CURRENT volume
        self._volumes.append(volume)

        if mean_vol == 0:
            return 1.0

        return volume / mean_vol
