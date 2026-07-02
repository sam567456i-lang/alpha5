"""Rule-based Decision Provider."""

from typing import Dict, Any, List
from Backend.methodology.signals import MethodologySignal
from .base import AbstractDecisionProvider, Decision


class RuleDecisionProvider(AbstractDecisionProvider):
    """
    Evaluates signals using deterministic logical rules.
    """

    def evaluate(self, signals: List[MethodologySignal], context: Dict[str, Any]) -> Decision:
        if not signals:
            return Decision(direction="WAIT", confidence=0.0, reason="No signals provided")

        # Simple rule: vote by highest confidence
        best_signal = max(signals, key=lambda s: s.confidence)
        
        if best_signal.confidence > 0.7:
            return Decision(
                direction=best_signal.direction,
                confidence=best_signal.confidence,
                reason=f"Rule matched strong {best_signal.direction} signal from {best_signal.methodology}",
                metadata={"voted_signal": best_signal.reason}
            )
            
        return Decision(direction="WAIT", confidence=0.0, reason="No strong signals")
