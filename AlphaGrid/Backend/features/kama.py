"""Kaufman's Adaptive Moving Average (KAMA)."""
from typing import Any, Dict, List, Optional
import math
from Shared.models.market import MarketSnapshot
from .base import AbstractFeature

class KAMAFeature(AbstractFeature):
    """
    Kaufman's Adaptive Moving Average (KAMA).
    Efficiency Ratio (ER) based adaptive MA.
    """
    
    def __init__(self, period: int = 10, fast_ema: int = 2, slow_ema: int = 30) -> None:
        self.period = period
        self.fast_alpha = 2 / (fast_ema + 1)
        self.slow_alpha = 2 / (slow_ema + 1)
        self._window: List[float] = []
        self._kama: Optional[float] = None
        
    @classmethod
    def get_name(cls) -> str:
        return "KAMA_10"

    @classmethod
    def get_version(cls) -> str:
        return "v1"

    @classmethod
    def get_dependencies(cls) -> List[str]:
        return []

    @classmethod
    def warmup_period(cls) -> int:
        return 10

    def compute(self, snapshot: MarketSnapshot, dependency_values: Dict[str, Any]) -> Optional[float]:
        price = float(snapshot.close)
        self._window.append(price)
        
        if len(self._window) > self.period + 1:
            self._window.pop(0)
            
        if len(self._window) < self.period + 1:
            if len(self._window) == self.period:
                # Initialize KAMA as SMA
                self._kama = sum(self._window) / self.period
            return None
            
        # Calculate Efficiency Ratio (ER)
        change = abs(self._window[-1] - self._window[0])
        volatility = sum(abs(self._window[i] - self._window[i-1]) for i in range(1, len(self._window)))
        
        if volatility == 0:
            er = 0.0
        else:
            er = change / volatility
            
        # Smoothing Constant (SC)
        sc = (er * (self.fast_alpha - self.slow_alpha) + self.slow_alpha) ** 2
        
        # Calculate KAMA
        self._kama = self._kama + sc * (price - self._kama)  # type: ignore
        return self._kama
