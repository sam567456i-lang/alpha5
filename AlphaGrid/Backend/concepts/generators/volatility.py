"""Volatility Concept Generator.

Interprets ATR and Relative Volume features to determine volatility state.
"""

from collections import deque
from typing import Any, Dict, List
from datetime import datetime
from Backend.concepts.base import Concept
from Backend.concepts.generator import AbstractConceptGenerator


class VolatilityConceptGenerator(AbstractConceptGenerator):
    """
    Generates a 'VolatilityState' Concept.
    Requires ATR_14 and RelativeVolume_5.
    """

    def __init__(self) -> None:
        self._atr_history = deque(maxlen=20)

    @classmethod
    def get_id(cls) -> str:
        return "VolatilityState"

    @classmethod
    def get_version(cls) -> str:
        return "v1"

    @classmethod
    def get_required_features(cls) -> List[str]:
        return ["ATR_14", "RelativeVolume_5"]

    def evaluate(self, timestamp: datetime, feature_values: Dict[str, Any]) -> Concept:
        atr = float(feature_values["ATR_14"])
        rvol = float(feature_values["RelativeVolume_5"])
        
        self._atr_history.append(atr)
        
        atr_expanding = len(self._atr_history) >= 3 and self._atr_history[-1] > self._atr_history[-3]
        atr_contracting = len(self._atr_history) >= 3 and self._atr_history[-1] < self._atr_history[-3]
        
        state = "NORMAL_VOLATILITY"
        confidence = 0.4

        if rvol > 1.5 and atr_expanding:
            state = "HIGH_VOLATILITY"
            confidence = min(1.0, rvol / 3.0)
        elif rvol < 0.7 and atr_contracting:
            state = "LOW_VOLATILITY"
            confidence = 0.6

        return Concept(
            id=self.get_id(),
            version=self.get_version(),
            timestamp=timestamp,
            confidence=confidence,
            inputs={
                "atr": atr, 
                "rvol": rvol, 
                "state": state, 
                "atr_expanding": atr_expanding,
                "atr_contracting": atr_contracting
            },
            generator=self.__class__.__name__
        )
