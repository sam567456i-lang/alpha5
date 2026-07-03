"""Hull Moving Average (HMA)."""
from typing import Any, Dict, List, Optional
import math
from Shared.models.market import MarketSnapshot
from .base import AbstractFeature

class WMA:
    def __init__(self, period: int):
        self.period = period
        self._window: List[float] = []
        self.denominator = period * (period + 1) / 2.0
        
    def add(self, price: float) -> Optional[float]:
        self._window.append(price)
        if len(self._window) > self.period:
            self._window.pop(0)
        
        if len(self._window) < self.period:
            return None
            
        numerator = sum((i + 1) * p for i, p in enumerate(self._window))
        return numerator / self.denominator

class HMAFeature(AbstractFeature):
    """
    Hull Moving Average (HMA).
    HMA = WMA(2*WMA(n/2) - WMA(n)), period = sqrt(n)
    """
    
    def __init__(self, period: int = 14) -> None:
        self.period = period
        self.half_period = int(period / 2)
        self.sqrt_period = int(math.sqrt(period))
        
        self._wma_full = WMA(self.period)
        self._wma_half = WMA(self.half_period)
        self._wma_sqrt = WMA(self.sqrt_period)
        
    @classmethod
    def get_name(cls) -> str:
        return "HMA_14"

    @classmethod
    def get_version(cls) -> str:
        return "v1"

    @classmethod
    def get_dependencies(cls) -> List[str]:
        return []

    @classmethod
    def warmup_period(cls) -> int:
        return 14 + int(math.sqrt(14))

    def compute(self, snapshot: MarketSnapshot, dependency_values: Dict[str, Any]) -> Optional[float]:
        price = float(snapshot.close)
        
        wma_f = self._wma_full.add(price)
        wma_h = self._wma_half.add(price)
        
        if wma_f is None or wma_h is None:
            return None
            
        raw_hma = 2 * wma_h - wma_f
        return self._wma_sqrt.add(raw_hma)
