"""Momentum Methodology."""

from Backend.methodology.base import AbstractMethodology
from Backend.methodology.evaluation import MethodologyEvaluation
from Backend.signals.primitive.context import SignalContext

class MomentumMethodology(AbstractMethodology):
    @classmethod
    def get_name(cls) -> str:
        return "Momentum"

    def evaluate(self, context: SignalContext) -> MethodologyEvaluation:
        momentums = context.get_signals("DIRECTIONAL_MOMENTUM")
        
        momentum = momentums[0] if momentums else None
        
        direction = 0
        confidence = 0.0
        is_active = False
        supporting = {}
        ts = None

        if momentum and momentum.direction != 0:
            ts = momentum.timestamp
            direction = momentum.direction
            confidence = momentum.confidence
            is_active = True
            supporting[momentum.id] = momentum.direction

        return MethodologyEvaluation(
            methodology_id=self.get_name(),
            timestamp=ts,
            is_active=is_active,
            direction=direction,
            confidence=confidence,
            supporting_concepts=supporting
        )
