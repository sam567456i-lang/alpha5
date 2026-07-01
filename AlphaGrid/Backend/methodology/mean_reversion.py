"""Mean Reversion Methodology."""

from typing import Dict, List
from Backend.concepts.base import Concept
from Backend.methodology.base import AbstractMethodology
from Backend.methodology.signals import Signal


class MeanReversionMethodology(AbstractMethodology):
    """
    Generates signals by identifying overextended momentum in stable volatility.
    """

    def get_name(self) -> str:
        return "MeanReversion"

    def get_required_concepts(self) -> List[str]:
        return ["MomentumState", "VolatilityState"]

    def evaluate(self, concepts: Dict[str, Concept]) -> Signal:
        momentum = concepts["MomentumState"]
        volatility = concepts["VolatilityState"]
        
        momentum_state = momentum.inputs.get("state", "NEUTRAL")
        vol_state = volatility.inputs.get("state", "NORMAL_VOLATILITY")
        
        # Do not fade high volatility breakouts
        if vol_state == "HIGH_VOLATILITY":
            return Signal(
                direction="WAIT",
                confidence=0.0,
                strength=0.0,
                reason="Volatility too high for mean reversion",
                concept_ids=self.get_required_concepts(),
                methodology=self.get_name(),
                provider="Rule"
            )
            
        # Buy oversold conditions
        if momentum_state == "OVERSOLD":
            return Signal(
                direction="LONG",
                confidence=momentum.confidence * 0.8, # Penalty for counter-trend
                strength=momentum.confidence,
                reason="Mean reversion buy on oversold conditions with stable volatility",
                concept_ids=self.get_required_concepts(),
                methodology=self.get_name(),
                provider="Rule"
            )
            
        # Sell overbought conditions
        if momentum_state == "OVERBOUGHT":
            return Signal(
                direction="SHORT",
                confidence=momentum.confidence * 0.8,
                strength=momentum.confidence,
                reason="Mean reversion sell on overbought conditions with stable volatility",
                concept_ids=self.get_required_concepts(),
                methodology=self.get_name(),
                provider="Rule"
            )
            
        return Signal(
            direction="WAIT",
            confidence=0.0,
            strength=0.0,
            reason="No actionable mean reversion setup",
            concept_ids=self.get_required_concepts(),
            methodology=self.get_name(),
            provider="Rule"
        )
