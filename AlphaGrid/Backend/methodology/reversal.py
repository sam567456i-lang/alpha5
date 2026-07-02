"""Reversal Methodology."""

from Backend.methodology.base import AbstractMethodology
from Backend.methodology.evaluation import MethodologyEvaluation
from Backend.signals.primitive.context import SignalContext

class ReversalMethodology(AbstractMethodology):
    @classmethod
    def get_name(cls) -> str:
        return "Reversal"

    def evaluate(self, context: SignalContext) -> MethodologyEvaluation:
        overextended_signals = context.get_signals("OVEREXTENDED")
        exhaustion_signals = context.get_signals("MOMENTUM_EXHAUSTION")
        
        overextended = overextended_signals[0] if overextended_signals else None
        exhaustion = exhaustion_signals[0] if exhaustion_signals else None
        
        direction = 0
        confidence = 0.0
        is_active = False
        supporting = {}
        ts = None

        if overextended and exhaustion:
            if overextended.direction == exhaustion.direction and overextended.direction != 0:
                ts = overextended.timestamp
                direction = -overextended.direction
                confidence = (overextended.confidence + exhaustion.confidence) / 2.0
                is_active = True
                supporting[overextended.id] = overextended.direction
                supporting[exhaustion.id] = exhaustion.direction

        return MethodologyEvaluation(
            methodology_id=self.get_name(),
            timestamp=ts,
            is_active=is_active,
            direction=direction,
            confidence=confidence,
            supporting_concepts=supporting
        )
