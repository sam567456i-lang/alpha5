"""SMA Crossover Primitive Signal Generator."""

from datetime import datetime
from typing import List, Optional
from Backend.concepts.base import Concept
from Backend.signals.primitive.base import AbstractPrimitiveSignalGenerator, PrimitiveSignal
from Shared.enums.concept_type import ConceptType

class SMACrossoverPrimitiveSignalGenerator(AbstractPrimitiveSignalGenerator):
    """
    Generates a STRONG_TREND signal based on the crossover of two SMA Trend Concepts.
    Consumes TrendState concepts generated from SMA features.
    """

    def __init__(self, fast_source: str = "SMA_10", slow_source: str = "SMA_20"):
        self.fast_source = fast_source
        self.slow_source = slow_source

    @classmethod
    def get_id(cls) -> str:
        return "SMA_CROSSOVER"

    @classmethod
    def get_required_concepts(cls) -> List[ConceptType]:
        return [ConceptType.TREND]

    def evaluate(self, timestamp: datetime, concepts: List[Concept]) -> Optional[PrimitiveSignal]:
        if not concepts:
            return None
            
        fast_concept = next((c for c in concepts if c.inputs.get("source") == self.fast_source), None)
        slow_concept = next((c for c in concepts if c.inputs.get("source") == self.slow_source), None)

        if not fast_concept or not slow_concept:
            return None

        fast_val = fast_concept.inputs.get("value")
        slow_val = slow_concept.inputs.get("value")

        if fast_val is None or slow_val is None:
            return None

        direction = 0
        if fast_val > slow_val:
            direction = 1
        elif fast_val < slow_val:
            direction = -1

        if direction != 0:
            return PrimitiveSignal(
                id=self.get_id(),
                timestamp=timestamp,
                direction=direction,
                confidence=0.8,
                supporting_concepts=(fast_concept.id, slow_concept.id),
                generator=self.__class__.__name__
            )

        return None
