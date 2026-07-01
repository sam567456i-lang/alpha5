"""Momentum Concept Generator.

Interprets RSI and ROC features to determine momentum state.
"""

from typing import Any, Dict, List
from datetime import datetime
from Backend.concepts.base import Concept
from Backend.concepts.generator import AbstractConceptGenerator


class MomentumConceptGenerator(AbstractConceptGenerator):
    """
    Generates a 'MomentumState' Concept.
    Requires ROC_5 and RSI_14.
    """

    @classmethod
    def get_id(cls) -> str:
        return "MomentumState"

    @classmethod
    def get_version(cls) -> str:
        return "v1"

    @classmethod
    def get_required_features(cls) -> List[str]:
        return ["ROC_5", "RSI_14"]

    def evaluate(self, timestamp: datetime, feature_values: Dict[str, Any]) -> Concept:
        roc = float(feature_values["ROC_5"])
        rsi = float(feature_values["RSI_14"])
        
        state = "MIXED"
        confidence = 0.4

        if rsi > 70 and roc > 0.02:
            state = "OVERBOUGHT"
            confidence = min(1.0, rsi / 100.0)
        elif rsi < 30 and roc < -0.02:
            state = "OVERSOLD"
            confidence = min(1.0, (100.0 - rsi) / 100.0)
        elif 40 < rsi < 60 and abs(roc) < 0.005:
            state = "NEUTRAL"
            confidence = 0.3

        return Concept(
            id=self.get_id(),
            version=self.get_version(),
            timestamp=timestamp,
            confidence=confidence,
            inputs={"roc": roc, "rsi": rsi, "state": state},
            generator=self.__class__.__name__
        )
