"""Ichimoku Cloud Features."""
from typing import Any, Dict, List, Optional
from Shared.models.market import MarketSnapshot
from .base import AbstractFeature

class BaseDonchianMidpoint(AbstractFeature):
    def __init__(self, period: int) -> None:
        self.period = period
        self._highs: List[float] = []
        self._lows: List[float] = []
        
    @classmethod
    def get_dependencies(cls) -> List[str]:
        return []

    def compute(self, snapshot: MarketSnapshot, dependency_values: Dict[str, Any]) -> Optional[float]:
        self._highs.append(float(snapshot.high))
        self._lows.append(float(snapshot.low))
        
        if len(self._highs) > self.period:
            self._highs.pop(0)
            self._lows.pop(0)
            
        if len(self._highs) < self.period:
            return None
            
        highest_high = max(self._highs)
        lowest_low = min(self._lows)
        return (highest_high + lowest_low) / 2.0

class TenkanSenFeature(BaseDonchianMidpoint):
    def __init__(self) -> None:
        super().__init__(period=9)

    @classmethod
    def get_name(cls) -> str:
        return "Tenkan_Sen"

    @classmethod
    def get_version(cls) -> str:
        return "v1"

    @classmethod
    def warmup_period(cls) -> int:
        return 9

class KijunSenFeature(BaseDonchianMidpoint):
    def __init__(self) -> None:
        super().__init__(period=26)

    @classmethod
    def get_name(cls) -> str:
        return "Kijun_Sen"

    @classmethod
    def get_version(cls) -> str:
        return "v1"

    @classmethod
    def warmup_period(cls) -> int:
        return 26

class SenkouSpanAFeature(AbstractFeature):
    """
    Senkou Span A = (Tenkan Sen + Kijun Sen) / 2
    Projected 26 periods ahead.
    """
    
    @classmethod
    def get_name(cls) -> str:
        return "Senkou_Span_A"

    @classmethod
    def get_version(cls) -> str:
        return "v1"

    @classmethod
    def get_dependencies(cls) -> List[str]:
        return ["Tenkan_Sen", "Kijun_Sen"]

    @classmethod
    def warmup_period(cls) -> int:
        return 26

    def compute(self, snapshot: MarketSnapshot, dependency_values: Dict[str, Any]) -> Optional[float]:
        tenkan = dependency_values.get("Tenkan_Sen")
        kijun = dependency_values.get("Kijun_Sen")
        if tenkan is None or kijun is None:
            return None
        return (tenkan + kijun) / 2.0

class SenkouSpanBFeature(BaseDonchianMidpoint):
    """
    Senkou Span B = 52-period Donchian Midpoint
    Projected 26 periods ahead.
    """
    def __init__(self) -> None:
        super().__init__(period=52)

    @classmethod
    def get_name(cls) -> str:
        return "Senkou_Span_B"

    @classmethod
    def get_version(cls) -> str:
        return "v1"

    @classmethod
    def warmup_period(cls) -> int:
        return 52
