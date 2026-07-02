"""Momentum Concept Generator.

Interprets dynamic momentum sources into semantic states:
INCREASING, WEAKENING, EXHAUSTED, ACCELERATING.
"""

from typing import Any, Dict, List, Deque, Optional
from collections import deque
from datetime import datetime
from Shared.enums.concept_type import ConceptType
from Shared.enums.concept_state import MomentumState
from Backend.concepts.base import Concept
from Backend.concepts.generator import AbstractConceptGenerator


class MomentumConceptGenerator(AbstractConceptGenerator):
    """
    Generates a 'MomentumState' Concept.
    Dynamically tracks the slope/acceleration of a given momentum source (e.g. MACD_Histogram, ROC_5).
    """

    def __init__(self, source: str, field: Optional[str] = None) -> None:
        self.source = source
        self.field = field
        self._history: Deque[float] = deque(maxlen=3)

    def get_id(self) -> str:
        return "MomentumState"

    def get_version(self) -> str:
        return "v2"

    def get_required_features(self) -> List[str]:
        return [self.source]

    def evaluate(self, timestamp: datetime, feature_values: Dict[str, Any]) -> Concept:
        feat = feature_values[self.source]
        val = float(feat[self.field]) if self.field and isinstance(feat, dict) else float(feat)
        self._history.append(val)
        
        state = MomentumState.UNKNOWN
        confidence = 0.5
        
        if len(self._history) < 3:
            return Concept(
                id=self.get_id(),
                type=ConceptType.MOMENTUM,
                version=self.get_version(),
                timestamp=timestamp,
                confidence=0.0,
                inputs={"source": self.source, "value": val, "state": "WARMING_UP"},
                generator=self.__class__.__name__
            )

        v0, v1, v2 = self._history[0], self._history[1], self._history[2]
        
        # Determine semantic state
        if v2 > v1 > v0:
            if (v2 - v1) > (v1 - v0):
                state = MomentumState.ACCELERATING
                confidence = 0.9
            else:
                state = MomentumState.INCREASING
                confidence = 0.7
        elif v2 < v1 < v0:
            if (v2 - v1) < (v1 - v0):
                state = MomentumState.ACCELERATING
                confidence = 0.9
            else:
                state = MomentumState.INCREASING
                confidence = 0.7
        elif v1 > v0 and v2 <= v1:
            state = MomentumState.WEAKENING
            confidence = 0.8
            if (v1 - v2) > abs(v1 - v0):
                state = MomentumState.EXHAUSTED
                confidence = 0.95
        elif v1 < v0 and v2 >= v1:
            state = MomentumState.WEAKENING
            confidence = 0.8
            if (v2 - v1) > abs(v1 - v0):
                state = MomentumState.EXHAUSTED
                confidence = 0.95
        else:
            state = MomentumState.UNKNOWN
            confidence = 0.3

        return Concept(
            id=self.get_id(),
            type=ConceptType.MOMENTUM,
            version=self.get_version(),
            timestamp=timestamp,
            confidence=confidence,
            inputs={"source": self.source, "value": val, "state": state},
            generator=self.__class__.__name__
        )
