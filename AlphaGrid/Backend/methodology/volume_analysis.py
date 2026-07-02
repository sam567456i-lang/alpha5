"""Volume Analysis Methodology."""

from Backend.methodology.base import AbstractMethodology
from Backend.methodology.evaluation import MethodologyEvaluation
from Backend.signals.primitive.context import SignalContext

class VolumeAnalysisMethodology(AbstractMethodology):
    @classmethod
    def get_name(cls) -> str:
        return "VolumeAnalysis"

    def evaluate(self, context: SignalContext) -> MethodologyEvaluation:
        surges = context.get_signals("VOLUME_SURGE")
        momentums = context.get_signals("DIRECTIONAL_MOMENTUM")
        
        surge = surges[0] if surges else None
        momentum = momentums[0] if momentums else None
        
        direction = 0
        confidence = 0.0
        is_active = False
        supporting = {}
        ts = None

        if surge and momentum and momentum.direction != 0:
            ts = surge.timestamp
            direction = momentum.direction
            confidence = (surge.confidence + momentum.confidence) / 2.0
            is_active = True
            supporting[surge.id] = surge.direction
            supporting[momentum.id] = momentum.direction

        return MethodologyEvaluation(
            methodology_id=self.get_name(),
            timestamp=ts,
            is_active=is_active,
            direction=direction,
            confidence=confidence,
            supporting_concepts=supporting
        )
