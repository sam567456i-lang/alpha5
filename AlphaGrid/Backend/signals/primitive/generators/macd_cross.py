"""MACD Cross Primitive Signal Generator."""

from datetime import datetime
from typing import List, Optional
from Backend.concepts.base import Concept
from Backend.signals.primitive.base import AbstractPrimitiveSignalGenerator, PrimitiveSignal
from Shared.enums.concept_type import ConceptType

class MACDCrossPrimitiveSignalGenerator(AbstractPrimitiveSignalGenerator):
    """
    Generates a MACD_CROSS signal based on the crossover of MACD Line and MACD Signal.
    Consumes TrendState concepts generated from MACD features.
    """

    def __init__(self, macd_line_source: str = "MACD_Line", macd_signal_source: str = "MACD_Signal"):
        self.macd_line_source = macd_line_source
        self.macd_signal_source = macd_signal_source

    @classmethod
    def get_id(cls) -> str:
        return "MACD_CROSS"

    @classmethod
    def get_required_concepts(cls) -> List[ConceptType]:
        return [ConceptType.TREND]

    def evaluate(self, timestamp: datetime, concepts: List[Concept]) -> Optional[PrimitiveSignal]:
        if not concepts:
            return None
            
        line_concept = next((c for c in concepts if c.inputs.get("source") == self.macd_line_source), None)
        signal_concept = next((c for c in concepts if c.inputs.get("source") == self.macd_signal_source), None)

        if not line_concept or not signal_concept:
            return None

        line_val = line_concept.inputs.get("value")
        signal_val = signal_concept.inputs.get("value")

        if line_val is None or signal_val is None:
            return None

        direction = 0
        if line_val > signal_val:
            direction = 1
        elif line_val < signal_val:
            direction = -1

        if direction != 0:
            return PrimitiveSignal(
                id=self.get_id(),
                timestamp=timestamp,
                direction=direction,
                confidence=0.8,
                supporting_concepts=(line_concept.id, signal_concept.id),
                generator=self.__class__.__name__
            )

        return None
