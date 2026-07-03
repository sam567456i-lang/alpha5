"""Trend Semantic Signal Generators."""

from datetime import datetime
from typing import List, Optional
import uuid

from Backend.concepts.base import Concept
from Backend.concepts.core.objects import TrendConcept
from Backend.signals.primitive.base import AbstractPrimitiveSignalGenerator, PrimitiveSignal
from Shared.enums.concept_type import ConceptType


class TrendSemanticSignalGenerator(AbstractPrimitiveSignalGenerator):
    """
    Evaluates TrendConcepts to generate semantic signals:
    TREND_LONG, TREND_SHORT, TREND_WEAKENING, TREND_STRENGTHENING.
    """

    @classmethod
    def get_id(cls) -> str:
        return "trend_semantic_v1"

    @classmethod
    def get_required_concepts(cls) -> List[ConceptType]:
        return [ConceptType.TREND]

    def evaluate(self, timestamp: datetime, concepts: List[Concept]) -> Optional[PrimitiveSignal]:
        # Filter down to TrendConcepts
        trend_concepts = [c for c in concepts if isinstance(c, TrendConcept)]
        if not trend_concepts:
            return None
            
        # For simplicity, we just use the most recent/relevant trend concept
        trend = trend_concepts[-1]
        
        signal_type = "TREND_NEUTRAL"
        direction = 0
        
        if trend.is_bullish:
            direction = 1
            if trend.trend_strength > 0.02: # arbitrarily defined strengthening threshold
                signal_type = "TREND_STRENGTHENING_LONG"
            else:
                signal_type = "TREND_LONG"
        else:
            direction = -1
            if trend.trend_strength > 0.02:
                signal_type = "TREND_STRENGTHENING_SHORT"
            else:
                signal_type = "TREND_SHORT"
                
        # Confidence could be derived from the trend strength itself
        confidence = min(trend.trend_strength * 10, 1.0)
                
        return PrimitiveSignal(
            id=str(uuid.uuid4()),
            timestamp=timestamp,
            direction=direction,
            confidence=confidence,
            signal_type=signal_type,
            supporting_concepts=(trend.id,),
            generator=self.get_id()
        )
