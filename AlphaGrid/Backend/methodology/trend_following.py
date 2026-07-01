"""Trend Following Methodology."""

from typing import Dict, List
from Backend.concepts.base import Concept
from Backend.methodology.base import AbstractMethodology
from Backend.methodology.signals import Signal


class TrendFollowingMethodology(AbstractMethodology):
    """
    Generates signals by confirming strong trends with non-exhausted momentum.
    """

    def get_name(self) -> str:
        return "TrendFollowing"

    def get_required_concepts(self) -> List[str]:
        return ["TrendState", "MomentumState"]

    def evaluate(self, concepts: Dict[str, Concept]) -> Signal:
        trend = concepts["TrendState"]
        momentum = concepts["MomentumState"]
        
        trend_state = trend.inputs.get("state", "NO_TREND")
        momentum_state = momentum.inputs.get("state", "NEUTRAL")
        
        # Bullish Trend Confirmation
        if trend_state == "BULLISH_TREND" and momentum_state != "OVERBOUGHT":
            return Signal(
                direction="LONG",
                confidence=(trend.confidence + momentum.confidence) / 2.0,
                strength=trend.confidence,
                reason="Bullish trend confirmed with non-overbought momentum",
                concept_ids=self.get_required_concepts(),
                methodology=self.get_name(),
                provider="Rule"
            )
            
        # Bearish Trend Confirmation
        if trend_state == "BEARISH_TREND" and momentum_state != "OVERSOLD":
            return Signal(
                direction="SHORT",
                confidence=(trend.confidence + momentum.confidence) / 2.0,
                strength=trend.confidence,
                reason="Bearish trend confirmed with non-oversold momentum",
                concept_ids=self.get_required_concepts(),
                methodology=self.get_name(),
                provider="Rule"
            )
            
        return Signal(
            direction="WAIT",
            confidence=0.0,
            strength=0.0,
            reason="No actionable trend signal",
            concept_ids=self.get_required_concepts(),
            methodology=self.get_name(),
            provider="Rule"
        )
