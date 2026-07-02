"""Breakout Methodology."""

from Backend.methodology.base import AbstractMethodology
from Backend.methodology.evaluation import MethodologyEvaluation
from Backend.signals.primitive.context import SignalContext

class BreakoutMethodology(AbstractMethodology):
    @classmethod
    def get_name(cls) -> str:
        return "Breakout"

    def evaluate(self, context: SignalContext) -> MethodologyEvaluation:
        breakouts = context.get_signals("BREAKOUT")
        breakout = breakouts[0] if breakouts else None
        
        direction = 0
        confidence = 0.0
        is_active = False
        supporting = {}
        ts = None

        if breakout and breakout.direction != 0:
            ts = breakout.timestamp
            direction = breakout.direction
            confidence = breakout.confidence
            is_active = True
            supporting[breakout.id] = breakout.direction

        return MethodologyEvaluation(
            methodology_id=self.get_name(),
            timestamp=ts,
            is_active=is_active,
            direction=direction,
            confidence=confidence,
            supporting_concepts=supporting
        )
