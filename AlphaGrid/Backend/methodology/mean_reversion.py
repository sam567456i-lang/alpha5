"""Mean Reversion Methodology."""

from Backend.methodology.base import AbstractMethodology
from Backend.methodology.evaluation import MethodologyEvaluation
from Backend.signals.primitive.context import SignalContext

class MeanReversionMethodology(AbstractMethodology):
    """
    Evaluates OVEREXTENDED primitive signals to produce a MethodologyEvaluation.
    Configurable via SignalContext (purely consumes primitive atomic observations).
    """

    @classmethod
    def get_name(cls) -> str:
        return "MeanReversion"

    def evaluate(self, context: SignalContext) -> MethodologyEvaluation:
        # Get primitive signals
        overextended_signals = context.get_signals("OVEREXTENDED")
        overextended = overextended_signals[0] if overextended_signals else None
        
        direction = 0
        confidence = 0.0
        is_active = False
        supporting = {}
        ts = None

        if overextended and overextended.direction != 0:
            ts = overextended.timestamp
            direction = -overextended.direction  # Revert against the overextension
            confidence = overextended.confidence
            is_active = True
            supporting[overextended.id] = overextended.direction

        return MethodologyEvaluation(
            methodology_id=self.get_name(),
            timestamp=ts,
            is_active=is_active,
            direction=direction,
            confidence=confidence,
            supporting_concepts=supporting
        )
