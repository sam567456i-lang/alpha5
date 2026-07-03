"""SuperTrend Flip Primitive Signal Generator."""

from datetime import datetime
from typing import List, Optional
from Backend.concepts.base import Concept
from Backend.signals.primitive.base import AbstractPrimitiveSignalGenerator, PrimitiveSignal
from Shared.enums.concept_type import ConceptType
from Shared.enums.concept_state import TrendState

class SuperTrendFlipPrimitiveSignalGenerator(AbstractPrimitiveSignalGenerator):
    """
    Generates a SUPERTREND_FLIP signal based on the TrendState of a SuperTrend feature.
    """

    def __init__(self, source: str = "SuperTrend"):
        self.source = source

    @classmethod
    def get_id(cls) -> str:
        return "SUPERTREND_FLIP"

    @classmethod
    def get_required_concepts(cls) -> List[ConceptType]:
        return [ConceptType.TREND]

    def evaluate(self, timestamp: datetime, concepts: List[Concept]) -> Optional[PrimitiveSignal]:
        if not concepts:
            return None
            
        st_concept = next((c for c in concepts if c.inputs.get("source") == self.source), None)

        if not st_concept:
            return None

        state = st_concept.inputs.get("state")

        direction = 0
        if state == TrendState.BULLISH:
            direction = 1
        elif state == TrendState.BEARISH:
            direction = -1

        if direction != 0:
            return PrimitiveSignal(
                id=self.get_id(),
                timestamp=timestamp,
                direction=direction,
                confidence=0.8,
                supporting_concepts=(st_concept.id,),
                generator=self.__class__.__name__
            )

        return None
