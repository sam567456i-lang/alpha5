"""Extremum Primitive Signal Generators."""

from datetime import datetime
from typing import List, Optional
from Backend.concepts.base import Concept
from Backend.signals.primitive.base import AbstractPrimitiveSignalGenerator, PrimitiveSignal
from Shared.enums.concept_type import ConceptType
from Shared.enums.concept_state import ExtremumState, VolatilityState

class OverextendedSignalGenerator(AbstractPrimitiveSignalGenerator):
    """
    Generates an Overextended signal if the extremum concept signals overbought/oversold.
    """

    @classmethod
    def get_id(cls) -> str:
        return "OVEREXTENDED"

    @classmethod
    def get_required_concepts(cls) -> List[ConceptType]:
        return [ConceptType.EXTREMUM, ConceptType.VOLATILITY]

    def evaluate(self, timestamp: datetime, concepts: List[Concept]) -> Optional[PrimitiveSignal]:
        extrema = [c for c in concepts if c.type == ConceptType.EXTREMUM]
        vols = [c for c in concepts if c.type == ConceptType.VOLATILITY]
        
        if not extrema or not vols:
            return None
            
        extremum = extrema[0]
        volatility = vols[0]
        
        ext_state = extremum.inputs.get("state", ExtremumState.UNKNOWN)
        vol_state = volatility.inputs.get("state", VolatilityState.UNKNOWN)
        
        direction = 0
        if ext_state == ExtremumState.OVEREXTENDED_BULLISH:
            direction = -1  # Overbought, expect bearish reversion
        elif ext_state == ExtremumState.OVEREXTENDED_BEARISH:
            direction = 1   # Oversold, expect bullish reversion
            
        # Volatility filter
        if vol_state == VolatilityState.EXPANDING:
            direction = 0  # Do not fade expanding volatility breakouts
            
        confidence = extremum.confidence
        if vol_state == VolatilityState.CONTRACTING:
            confidence = min(1.0, confidence * 1.2)
            
        if direction != 0:
            return PrimitiveSignal(
                id=self.get_id(),
                timestamp=timestamp,
                direction=direction,
                confidence=confidence,
                supporting_concepts=(extremum.id, volatility.id),
                generator=self.get_id()
            )
            
        return None
