"""Trend Primitive Signal Generators."""

from datetime import datetime
from typing import List, Optional
from Backend.concepts.base import Concept
from Backend.signals.primitive.base import AbstractPrimitiveSignalGenerator, PrimitiveSignal
from Shared.enums.concept_type import ConceptType
from Shared.enums.concept_state import TrendState, StrengthState

class StrongTrendSignalGenerator(AbstractPrimitiveSignalGenerator):
    """
    Generates a StrongTrend signal if the trend is directional AND strength is strong.
    """

    @classmethod
    def get_id(cls) -> str:
        return "STRONG_TREND"

    @classmethod
    def get_required_concepts(cls) -> List[ConceptType]:
        return [ConceptType.TREND, ConceptType.STRENGTH]

    def evaluate(self, timestamp: datetime, concepts: List[Concept]) -> Optional[PrimitiveSignal]:
        trends = [c for c in concepts if c.type == ConceptType.TREND]
        strengths = [c for c in concepts if c.type == ConceptType.STRENGTH]
        
        if not trends or not strengths:
            return None
            
        trend = trends[0]
        strength = strengths[0]
        
        trend_state = trend.inputs.get("state", TrendState.UNKNOWN)
        str_state = strength.inputs.get("state", StrengthState.UNKNOWN)
        
        direction = 0
        if str_state == StrengthState.STRONG:
            if trend_state == TrendState.BULLISH:
                direction = 1
            elif trend_state == TrendState.BEARISH:
                direction = -1
                
        if direction != 0:
            confidence = trend.confidence * strength.confidence
            return PrimitiveSignal(
                id=self.get_id(),
                timestamp=timestamp,
                direction=direction,
                confidence=confidence,
                supporting_concepts=(trend.id, strength.id),
                generator=self.get_id()
            )
            
        return None
