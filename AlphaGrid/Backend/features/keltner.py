"""Keltner Channels Feature."""

from typing import Any, Dict, List
from Shared.models.market import MarketSnapshot
from .base import AbstractFeature

class KeltnerChannelFeature(AbstractFeature):
    """
    Computes Keltner Channels based on EMA and ATR.
    O(n) streaming calculation.
    """

    def __init__(self, period: int = 20, multiplier: float = 2.0) -> None:
        self.period = period
        self.multiplier = multiplier

    @classmethod
    def get_name(cls) -> str:
        return "Keltner_20_2"

    @classmethod
    def get_version(cls) -> str:
        return "v1"

    @classmethod
    def get_dependencies(cls) -> List[str]:
        return ["EMA_20", "ATR_14"]

    @classmethod
    def warmup_period(cls) -> int:
        return 20

    def compute(self, snapshot: MarketSnapshot, dependency_values: Dict[str, Any]) -> Any:
        ema = dependency_values.get("EMA_20")
        atr = dependency_values.get("ATR_14")
        
        if ema is None or atr is None:
            return None

        upper = ema + (self.multiplier * atr)
        lower = ema - (self.multiplier * atr)

        return {
            "ema": ema,
            "upper_band": upper,
            "lower_band": lower
        }
