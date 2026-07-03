"""Ichimoku Breakout Primitive Signal Generator."""

from datetime import datetime
from typing import List, Optional
from Backend.concepts.base import Concept
from Backend.signals.primitive.base import AbstractPrimitiveSignalGenerator, PrimitiveSignal
from Shared.enums.concept_type import ConceptType

class IchimokuBreakoutPrimitiveSignalGenerator(AbstractPrimitiveSignalGenerator):
    """
    Generates an ICHIMOKU_BREAKOUT signal based on Price relation to the Cloud (Senkou Span A and B).
    """

    def __init__(self, span_a_source: str = "Senkou_Span_A", span_b_source: str = "Senkou_Span_B"):
        self.span_a_source = span_a_source
        self.span_b_source = span_b_source

    @classmethod
    def get_id(cls) -> str:
        return "ICHIMOKU_BREAKOUT"

    @classmethod
    def get_required_concepts(cls) -> List[ConceptType]:
        return [ConceptType.TREND]

    def evaluate(self, timestamp: datetime, concepts: List[Concept]) -> Optional[PrimitiveSignal]:
        if not concepts:
            return None
            
        span_a_concept = next((c for c in concepts if c.inputs.get("source") == self.span_a_source), None)
        span_b_concept = next((c for c in concepts if c.inputs.get("source") == self.span_b_source), None)

        if not span_a_concept or not span_b_concept:
            return None

        # The trend generator injects price as the input value if we're using fallback price comparison,
        # but Senkou span A and B are future projections, so typically we just compare price vs them.
        # Here we assume the TrendConceptGenerator has set 'value' to the span value, and we just need
        # to know if the current price is above BOTH.
        # Actually, if we use TrendConceptGenerator, it sets TrendState based on Price > Value.
        # So we can just check if BOTH states are BULLISH.
        from Shared.enums.concept_state import TrendState
        
        a_state = span_a_concept.inputs.get("state")
        b_state = span_b_concept.inputs.get("state")

        direction = 0
        if a_state == TrendState.BULLISH and b_state == TrendState.BULLISH:
            direction = 1
        elif a_state == TrendState.BEARISH and b_state == TrendState.BEARISH:
            direction = -1

        if direction != 0:
            return PrimitiveSignal(
                id=self.get_id(),
                timestamp=timestamp,
                direction=direction,
                confidence=0.8,
                supporting_concepts=(span_a_concept.id, span_b_concept.id),
                generator=self.__class__.__name__
            )

        return None
