"""Volatility Primitive Signal Generators."""

from datetime import datetime
from typing import List, Optional
from Backend.concepts.base import Concept
from Backend.signals.primitive.base import AbstractPrimitiveSignalGenerator, PrimitiveSignal
from Shared.enums.concept_type import ConceptType
from Shared.enums.concept_state import VolatilityState

class VolatilityExpansionSignalGenerator(AbstractPrimitiveSignalGenerator):
    """
    Generates a VOLATILITY_EXPANSION signal when the volatility concept detects EXPANDING state.
    """

    @classmethod
    def get_id(cls) -> str:
        return "VOLATILITY_EXPANSION"

    @classmethod
    def get_required_concepts(cls) -> List[ConceptType]:
        return [ConceptType.VOLATILITY]

    def evaluate(self, timestamp: datetime, concepts: List[Concept]) -> Optional[PrimitiveSignal]:
        vols = [c for c in concepts if c.type == ConceptType.VOLATILITY]
        
        if not vols:
            return None
            
        volatility = vols[0]
        state = volatility.inputs.get("state", VolatilityState.UNKNOWN)
        
        if state == VolatilityState.EXPANDING:
            return PrimitiveSignal(
                id=self.get_id(),
                timestamp=timestamp,
                direction=0, # Volatility expansion is non-directional
                confidence=volatility.confidence,
                supporting_concepts=(volatility.id,),
                generator=self.get_id()
            )
            
        return None
