"""Trend Concept Generator.

Interprets EMA and SMA features to determine trend state.
"""

from typing import Any, Dict, List
from datetime import datetime
from Backend.concepts.base import Concept
from Backend.concepts.generator import AbstractConceptGenerator


class TrendConceptGenerator(AbstractConceptGenerator):
    """
    Generates a 'TrendState' Concept.
    Requires EMA_20 and SMA_20.
    """

    @classmethod
    def get_id(cls) -> str:
        return "TrendState"

    @classmethod
    def get_version(cls) -> str:
        return "v1"

    @classmethod
    def get_required_features(cls) -> List[str]:
        return ["EMA_20", "SMA_20"]

    def evaluate(self, timestamp: datetime, feature_values: Dict[str, Any]) -> Concept:
        ema = float(feature_values["EMA_20"])
        sma = float(feature_values["SMA_20"])
        
        spread_pct = ((ema - sma) / sma * 100.0) if sma != 0 else 0.0
        
        state = "NO_TREND"
        confidence = 0.2

        if spread_pct > 0.5:
            state = "BULLISH_TREND"
            confidence = min(1.0, abs(spread_pct) / 3.0)
        elif spread_pct < -0.5:
            state = "BEARISH_TREND"
            confidence = min(1.0, abs(spread_pct) / 3.0)

        return Concept(
            id=self.get_id(),
            version=self.get_version(),
            timestamp=timestamp,
            confidence=confidence,
            inputs={"ema": ema, "sma": sma, "spread_pct": spread_pct, "state": state},
            generator=self.__class__.__name__
        )
