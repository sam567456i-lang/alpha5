"""Breakout Primitive Signal Generators."""

from datetime import datetime
from typing import List, Optional
from Backend.concepts.base import Concept
from Backend.signals.primitive.base import AbstractPrimitiveSignalGenerator, PrimitiveSignal
from Shared.enums.concept_type import ConceptType
from Shared.enums.concept_state import BreakoutState, VolatilityState

class BreakoutSignalGenerator(AbstractPrimitiveSignalGenerator):
    """
    Generates a Breakout signal if the breakout concept signals a bullish/bearish breakout and volatility is expanding.
    """

    @classmethod
    def get_id(cls) -> str:
        return "BREAKOUT"

    @classmethod
    def get_required_concepts(cls) -> List[ConceptType]:
        return [ConceptType.BREAKOUT, ConceptType.VOLATILITY]

    def evaluate(self, timestamp: datetime, concepts: List[Concept]) -> Optional[PrimitiveSignal]:
        breakouts = [c for c in concepts if c.type == ConceptType.BREAKOUT]
        vols = [c for c in concepts if c.type == ConceptType.VOLATILITY]
        
        if not breakouts or not vols:
            return None
            
        breakout = breakouts[0]
        volatility = vols[0]
        state = breakout.inputs.get("state", BreakoutState.UNKNOWN)
        vol_state = volatility.inputs.get("state", VolatilityState.UNKNOWN)
        
        direction = 0
        if vol_state == VolatilityState.EXPANDING:
            if state == BreakoutState.BULLISH_BREAKOUT:
                direction = 1
            elif state == BreakoutState.BEARISH_BREAKOUT:
                direction = -1
            
        if direction != 0:
            return PrimitiveSignal(
                id=self.get_id(),
                timestamp=timestamp,
                direction=direction,
                confidence=min(1.0, breakout.confidence * volatility.confidence * 1.5),
                supporting_concepts=(breakout.id, volatility.id),
                generator=self.get_id()
            )
            
        return None
