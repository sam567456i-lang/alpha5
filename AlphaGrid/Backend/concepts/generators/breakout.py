"""Breakout Concept Generator."""

from typing import Any, Dict, List
from datetime import datetime
from Backend.concepts.base import Concept
from Backend.concepts.generator import AbstractConceptGenerator
from Shared.enums.concept_state import BreakoutState
from Shared.enums.concept_type import ConceptType

class BreakoutConceptGenerator(AbstractConceptGenerator):
    """
    Evaluates price action against arbitrary channel bounds (e.g. Bollinger, Donchian, Keltner).
    """

    def __init__(
        self, 
        source: str, 
        upper_band_field: str = "upper_band", 
        lower_band_field: str = "lower_band",
        price_field: str = "close"
    ) -> None:
        """
        Args:
            source: The feature name (e.g., 'Donchian_20', 'Bollinger_Metrics')
            upper_band_field: Field name for the upper band.
            lower_band_field: Field name for the lower band.
            price_field: Field name for the price value in the feature output.
        """
        self.source = source
        self.upper_band_field = upper_band_field
        self.lower_band_field = lower_band_field
        self.price_field = price_field

    def get_id(self) -> str:
        return f"BreakoutState_{self.source}"

    def get_version(self) -> str:
        return "v2"

    def get_required_features(self) -> List[str]:
        return [self.source]

    def evaluate(self, timestamp: datetime, feature_values: Dict[str, Any], geometry_cache: Any = None) -> Concept:
        feat = feature_values[self.source]
        
        upper = float(feat[self.upper_band_field])
        lower = float(feat[self.lower_band_field])
        price = float(feat[self.price_field])
        
        state = BreakoutState.NO_BREAKOUT
        confidence = 0.5
        
        if price >= upper and price > 0.0:
            state = BreakoutState.BULLISH_BREAKOUT
            confidence = 0.9
        elif price <= lower and price > 0.0:
            state = BreakoutState.BEARISH_BREAKOUT
            confidence = 0.9
            
        return Concept(
            id=self.get_id(),
            type=ConceptType.BREAKOUT,
            version=self.get_version(),
            timestamp=timestamp,
            confidence=confidence,
            inputs={"source": self.source, "value": price, "state": state},
            generator=self.__class__.__name__
        )
