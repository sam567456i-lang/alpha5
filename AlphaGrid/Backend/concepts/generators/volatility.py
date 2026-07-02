"""Volatility Concept Generator."""

from typing import Any, Dict, List, Deque
from collections import deque
from datetime import datetime
from Backend.concepts.base import Concept
from Shared.enums.concept_state import VolatilityState
from Shared.enums.concept_type import ConceptType
from Backend.concepts.generator import AbstractConceptGenerator


class VolatilityConceptGenerator(AbstractConceptGenerator):
    """
    Generates a 'VolatilityState' Concept.
    Dynamically maps a volatility source (e.g. Bollinger_Metrics -> band_width) 
    to EXPANDING, CONTRACTING, NORMAL.
    """

    def __init__(self, source: str, field: str | None = None) -> None:

        """
        Args:
            source: The feature name (e.g., 'Bollinger_Metrics' or 'ATR_14')
            field: Optional sub-field if the feature returns a dict (e.g., 'band_width')
        """
        self.source = source
        self.field = field
        self._history: Deque[float] = deque(maxlen=20)

    def get_id(self) -> str:
        return "VolatilityState"

    def get_version(self) -> str:
        return "v2"

    def get_required_features(self) -> List[str]:
        return [self.source]

    def evaluate(self, timestamp: datetime, feature_values: Dict[str, Any]) -> Concept:
        feat = feature_values[self.source]
        val = float(feat[self.field]) if self.field and isinstance(feat, dict) else float(feat)
        
        self._history.append(val)
        
        if len(self._history) < 20:
            return Concept(
                id=self.get_id(),
                type=ConceptType.VOLATILITY,
                version=self.get_version(),
                timestamp=timestamp,
                confidence=0.0,
                inputs={"source": self.source, "value": val, "state": VolatilityState.WARMING_UP},
                generator=self.__class__.__name__
            )

        mean_vol = sum(self._history) / 20.0
        current_vol = val
        
        state = VolatilityState.NORMAL
        confidence = 0.5
        
        if current_vol > mean_vol * 1.5:
            state = VolatilityState.EXPANDING
            confidence = 0.9
        elif current_vol < mean_vol * 0.5:
            state = VolatilityState.CONTRACTING
            confidence = 0.9
        elif current_vol > mean_vol * 1.2:
            state = VolatilityState.EXPANDING
            confidence = 0.7
        elif current_vol < mean_vol * 0.8:
            state = VolatilityState.CONTRACTING
            confidence = 0.7

        return Concept(
            id=self.get_id(),
            type=ConceptType.VOLATILITY,
            version=self.get_version(),
            timestamp=timestamp,
            confidence=confidence,
            inputs={"source": self.source, "value": val, "state": state},
            generator=self.__class__.__name__
        )
