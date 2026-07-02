"""Trend Following Methodology."""

from Backend.methodology.base import AbstractMethodology
from Backend.methodology.evaluation import MethodologyEvaluation
from Backend.signals.primitive.context import SignalContext

class TrendFollowingMethodology(AbstractMethodology):
    """
    Evaluates StrongTrend and DirectionalMomentum primitive signals to produce a MethodologyEvaluation.
    Configurable via SignalContext (purely consumes primitive atomic observations).
    """

    @classmethod
    def get_name(cls) -> str:
        return "TrendFollowing"

    def evaluate(self, context: SignalContext) -> MethodologyEvaluation:
        # Get primitive signals
        strong_trends = context.get_signals("STRONG_TREND")
        directional_momentums = context.get_signals("DIRECTIONAL_MOMENTUM")
        
        strong_trend = strong_trends[0] if strong_trends else None
        directional_momentum = directional_momentums[0] if directional_momentums else None
        
        direction = 0
        confidence = 0.0
        is_active = False
        
        supporting = {}
        ts = None

        if strong_trend and strong_trend.direction != 0:
            ts = strong_trend.timestamp
            direction = strong_trend.direction
            confidence = strong_trend.confidence
            is_active = True
            supporting[strong_trend.id] = strong_trend.direction
            
        if directional_momentum and directional_momentum.direction != 0:
            ts = ts or directional_momentum.timestamp
            supporting[directional_momentum.id] = directional_momentum.direction
            if is_active:
                # Require momentum to align with trend
                if directional_momentum.direction == direction:
                    confidence = min(1.0, confidence + (directional_momentum.confidence * 0.2))
                else:
                    is_active = False  # Momentum contradicts strong trend
                    direction = 0
            else:
                # Momentum alone might not be enough, but for this strategy we will allow it with lower confidence
                direction = directional_momentum.direction
                confidence = directional_momentum.confidence * 0.5
                is_active = True

        return MethodologyEvaluation(
            methodology_id=self.get_name(),
            timestamp=ts,

            is_active=is_active,
            direction=direction,
            confidence=confidence,
            supporting_concepts=supporting
        )
