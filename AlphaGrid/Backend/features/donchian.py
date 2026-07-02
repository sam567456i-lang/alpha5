"""
Donchian Channel Feature.

Provides atomic feature primitives for Donchian Channels.
"""

from typing import Any, Dict, List
from collections import deque
from Shared.models.market import MarketSnapshot
from Backend.features.base import AbstractFeature

class Donchian20Feature(AbstractFeature):
    """
    Computes the 20-period Donchian Channels.
    """
    
    def __init__(self) -> None:
        self.period = 20
        self._highs: deque[float] = deque(maxlen=self.period)
        self._lows: deque[float] = deque(maxlen=self.period)
        
    @classmethod
    def get_name(cls) -> str:
        return "Donchian_20"
        
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
        high = float(snapshot.high)
        low = float(snapshot.low)
        close = float(snapshot.close)
        
        self._highs.append(high)
        self._lows.append(low)
        
        if len(self._highs) < self.period:
            return None
            
        upper = max(self._highs)
        lower = min(self._lows)
        middle = (upper + lower) / 2.0
        
        return {
            "upper_band": upper,
            "lower_band": lower,
            "middle_band": middle,
            "band_width": upper - lower,
            "close": close
        }
