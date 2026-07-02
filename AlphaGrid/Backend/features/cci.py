"""Commodity Channel Index (CCI) Feature."""

from collections import deque
from typing import Any, Dict, List
from Shared.models.market import MarketSnapshot
from .base import AbstractFeature

class CCIFeature(AbstractFeature):
    """
    Computes Commodity Channel Index (CCI).
    O(n) streaming calculation using a sliding window for SMA and Mean Deviation.
    """

    def __init__(self, period: int = 20) -> None:
        self.period = period
        self._typical_prices = deque(maxlen=period)  # type: ignore

    @classmethod
    def get_name(cls) -> str:
        return "CCI_20"

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
        tp = (float(snapshot.high) + float(snapshot.low) + float(snapshot.close)) / 3.0
        
        self._typical_prices.append(tp)
        
        if len(self._typical_prices) < self.period:
            return None
            
        sma = sum(self._typical_prices) / self.period
        
        mean_deviation = sum(abs(p - sma) for p in self._typical_prices) / self.period
        
        if mean_deviation == 0:
            return 0.0
            
        cci = (tp - sma) / (0.015 * mean_deviation)
        return cci
