"""Momentum Primitive Signal Generators."""

from datetime import datetime
from typing import List, Optional
from Backend.concepts.base import Concept
from Backend.signals.primitive.base import AbstractPrimitiveSignalGenerator, PrimitiveSignal
from Shared.enums.concept_type import ConceptType
from Shared.enums.concept_state import MomentumState

class MomentumSignalGenerator(AbstractPrimitiveSignalGenerator):
    """
    Generates a DirectionalMomentum signal if momentum is accelerating or increasing.
    """

    @classmethod
    def get_id(cls) -> str:
        return "DIRECTIONAL_MOMENTUM"

    @classmethod
    def get_required_concepts(cls) -> List[ConceptType]:
        return [ConceptType.MOMENTUM]

    def evaluate(self, timestamp: datetime, concepts: List[Concept]) -> Optional[PrimitiveSignal]:
        momentums = [c for c in concepts if c.type == ConceptType.MOMENTUM]
        
        if not momentums:
            return None
            
        momentum = momentums[0]
        mom_state = momentum.inputs.get("state", MomentumState.UNKNOWN)
        
        direction = 0
        if mom_state in [MomentumState.ACCELERATING, MomentumState.INCREASING]:
            val = momentum.inputs.get("value", 0)
            if val > 0:
                direction = 1
            elif val < 0:
                direction = -1
                
        if direction != 0:
            return PrimitiveSignal(
                id=self.get_id(),
                timestamp=timestamp,
                direction=direction,
                confidence=momentum.confidence,
                supporting_concepts=(momentum.id,),
                generator=self.get_id()
            )
            
        return None


class MomentumExhaustionSignalGenerator(AbstractPrimitiveSignalGenerator):
    """
    Generates a MomentumExhaustion signal if momentum is weakening or exhausted.
    """

    @classmethod
    def get_id(cls) -> str:
        return "MOMENTUM_EXHAUSTION"

    @classmethod
    def get_required_concepts(cls) -> List[ConceptType]:
        return [ConceptType.MOMENTUM]

    def evaluate(self, timestamp: datetime, concepts: List[Concept]) -> Optional[PrimitiveSignal]:
        momentums = [c for c in concepts if c.type == ConceptType.MOMENTUM]
        
        if not momentums:
            return None
            
        momentum = momentums[0]
        mom_state = momentum.inputs.get("state", MomentumState.UNKNOWN)
        
        direction = 0
        if mom_state in [MomentumState.WEAKENING, MomentumState.EXHAUSTED]:
            val = momentum.inputs.get("value", 0)
            if val > 0:
                direction = -1 # Bullish momentum exhausted, expect bearish
            elif val < 0:
                direction = 1  # Bearish momentum exhausted, expect bullish
                
        if direction != 0:
            return PrimitiveSignal(
                id=self.get_id(),
                timestamp=timestamp,
                direction=direction,
                confidence=momentum.confidence,
                supporting_concepts=(momentum.id,),
                generator=self.get_id()
            )
            
        return None
