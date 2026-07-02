"""Stochastic Oscillator Feature."""

from collections import deque
from typing import Any, Dict, List
from Shared.models.market import MarketSnapshot
from .base import AbstractFeature

class StochasticFeature(AbstractFeature):
    """
    Computes Stochastic Oscillator (%K and %D).
    O(n) streaming calculation using sliding windows.
    """

    def __init__(self, k_period: int = 14, d_period: int = 3) -> None:
        self.k_period = k_period
        self.d_period = d_period
        self._highs = deque(maxlen=k_period)  # type: ignore
        self._lows = deque(maxlen=k_period)  # type: ignore
        self._k_values = deque(maxlen=d_period)  # type: ignore

    @classmethod
    def get_name(cls) -> str:
        return "Stochastic_14_3"

    @classmethod
    def get_version(cls) -> str:
        return "v1"

    @classmethod
    def get_dependencies(cls) -> List[str]:
        return []

    @classmethod
    def warmup_period(cls) -> int:
        return 14 + 3 - 1

    def compute(self, snapshot: MarketSnapshot, dependency_values: Dict[str, Any]) -> Any:
        high = float(snapshot.high)
        low = float(snapshot.low)
        close = float(snapshot.close)
        
        self._highs.append(high)
        self._lows.append(low)
        
        if len(self._highs) < self.k_period:
            return None
            
        hh = max(self._highs)
        ll = min(self._lows)
        
        if hh == ll:
            k = 50.0
        else:
            k = ((close - ll) / (hh - ll)) * 100.0
            
        self._k_values.append(k)
        
        if len(self._k_values) < self.d_period:
            return None
            
        d = sum(self._k_values) / self.d_period
        
        return {"k": k, "d": d}
