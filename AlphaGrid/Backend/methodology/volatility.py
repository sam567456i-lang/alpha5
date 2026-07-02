"""Volatility Methodology."""

from Backend.methodology.base import AbstractMethodology
from Backend.methodology.evaluation import MethodologyEvaluation
from Backend.signals.primitive.context import SignalContext

class VolatilityMethodology(AbstractMethodology):
    @classmethod
    def get_name(cls) -> str:
        return "Volatility"

    def evaluate(self, context: SignalContext) -> MethodologyEvaluation:
        expansions = context.get_signals("VOLATILITY_EXPANSION")
        momentums = context.get_signals("DIRECTIONAL_MOMENTUM")
        
        expansion = expansions[0] if expansions else None
        momentum = momentums[0] if momentums else None
        
        direction = 0
        confidence = 0.0
        is_active = False
        supporting = {}
        ts = None

        if expansion and momentum and momentum.direction != 0:
            ts = expansion.timestamp
            direction = momentum.direction
            confidence = (expansion.confidence + momentum.confidence) / 2.0
            is_active = True
            supporting[expansion.id] = expansion.direction
            supporting[momentum.id] = momentum.direction

        return MethodologyEvaluation(
            methodology_id=self.get_name(),
            timestamp=ts,
            is_active=is_active,
            direction=direction,
            confidence=confidence,
            supporting_concepts=supporting
        )
