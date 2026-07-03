"""Trend Concept Generator."""

from typing import Any, Dict, List
from datetime import datetime
from Backend.concepts.base import Concept
from Shared.enums.concept_state import TrendState
from Shared.enums.concept_type import ConceptType
from Shared.enums.signal_direction import SignalDirection
from Backend.concepts.generator import AbstractConceptGenerator


class TrendConceptGenerator(AbstractConceptGenerator):
    """
    Generates a 'TrendState' Concept.
    Dynamically consumes either a standardized TrendFeatureOutput protocol (like SuperTrend)
    or compares price against a given trend source (like SMA).
    """

    def __init__(self, source: str, price_field: str = "close") -> None:
        """
        Args:
            source: The moving average or trend feature ID to consume.
            price_field: Field to compare against if the feature just emits a value.
        """
        self.source = source
        self.price_field = price_field

    def get_id(self) -> str:
        return f"TrendState_{self.source}"

    def get_version(self) -> str:
        return "v3"

    def get_required_features(self) -> List[str]:
        return [self.source]

    def evaluate(self, timestamp: datetime, feature_values: Dict[str, Any], geometry_cache: Any = None) -> Concept:
        feat = feature_values[self.source]
        
        state = TrendState.UNKNOWN
        confidence = 0.5
        val = 0.0
        
        # Check if the feature output implements the TrendFeatureOutput protocol directly (or via dict)
        if hasattr(feat, "direction"):
            direction = feat.direction
            val = getattr(feat, "supertrend", 0.0) # Extract underlying value if any
            
            if direction == SignalDirection.LONG:
                state = TrendState.BULLISH
                confidence = 0.8
            elif direction == SignalDirection.SHORT:
                state = TrendState.BEARISH
                confidence = 0.8
        elif isinstance(feat, dict) and "direction" in feat:
            direction = feat["direction"]
            val = feat.get("supertrend", 0.0)
            
            if direction == SignalDirection.LONG:
                state = TrendState.BULLISH
                confidence = 0.8
            elif direction == SignalDirection.SHORT:
                state = TrendState.BEARISH
                confidence = 0.8
        else:
            # Fallback to simple price vs MA comparison
            trend_val = float(feat) if not isinstance(feat, dict) else float(feat.get("ema", feat.get("sma", 0.0)))  # type: ignore
            val = trend_val
            price = float(feature_values.get(self.price_field, 0.0))
            
            if price > trend_val and price > 0.0:
                state = TrendState.BULLISH
                confidence = 0.6
            elif price < trend_val and price > 0.0:
                state = TrendState.BEARISH
                confidence = 0.6

        return Concept(
            id=self.get_id(),
            type=ConceptType.TREND,
            version=self.get_version(),
            timestamp=timestamp,
            confidence=confidence,
            inputs={"source": self.source, "value": val, "state": state},
            generator=self.__class__.__name__
        )
