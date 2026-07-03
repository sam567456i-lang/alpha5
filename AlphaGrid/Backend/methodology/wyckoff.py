"""Wyckoff Methodology."""

from typing import Dict, Any
from Backend.methodology.base import AbstractMethodology
from Backend.methodology.evaluation import MethodologyEvaluation
from Backend.signals.primitive.context import SignalContext

class WyckoffMethodology(AbstractMethodology):
    """
    Wyckoff Methodology interprets generic market structure primitives to identify
    Accumulation/Distribution phases (e.g., Springs, Upthrusts, Signs of Strength).
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        # Wyckoff-specific weighting
        self.weights = self.config.get("weights", {
            "spring_or_upthrust": 0.40,
            "sos_or_sow": 0.35,  # Sign of Strength / Sign of Weakness (BOS/CHOCH)
            "test": 0.25         # Retest / OB Mitigation
        })

    @classmethod
    def get_name(cls) -> str:
        return "Wyckoff"

    def evaluate(self, context: SignalContext) -> MethodologyEvaluation:
        # Retrieve the generic composite primitive signal
        signals = context.get_signals("MARKET_STRUCTURE_EVENT")
        if not signals:
            return MethodologyEvaluation(
                methodology_id=self.get_name(),
                timestamp=None,
                is_active=False,
                direction=0,
                confidence=0.0
            )
            
        latest_signal = signals[-1]
        events = latest_signal.metadata
        
        # We start neutral unless we see strong Wyckoff events
        direction = 0
        confidence = 0.0
        supporting_concepts = {}
        
        # A simple Wyckoff interpretation:
        # 1. A Liquidity Sweep (Pools swept) followed by a CHOCH is a "Spring" or "Upthrust".
        pools_active = events.get("active_pools", 0)
        has_structure = "structure" in events
        struct_is_bullish = events["structure"]["is_bullish"] if has_structure else False
        
        # Mock logic for Spring: Low pools swept + Bullish CHOCH (Sign of Strength)
        if has_structure and events["structure"]["type"] == "CHOCH":
            direction = 1 if struct_is_bullish else -1
            confidence += self.weights["sos_or_sow"]
            supporting_concepts["SOS" if direction == 1 else "SOW"] = 1
            
            # If there was a liquidity event, it acts as the Spring (bullish) or Upthrust (bearish)
            if pools_active > 0: # Proxy for liquidity context in this mock
                confidence += self.weights["spring_or_upthrust"]
                supporting_concepts["SPRING" if direction == 1 else "UPTHRUST"] = 1
                
        # 2. Retest / Mitigation of the origin of the SOS/SOW
        if events.get("ob_mitigated"):
            ob_bullish = events.get("ob_bullish")
            if direction == 0:
                direction = 1 if ob_bullish else -1
            
            if (direction == 1 and ob_bullish) or (direction == -1 and not ob_bullish):
                confidence += self.weights["test"]
                supporting_concepts["TEST"] = 1

        is_active = confidence >= 0.50 # Require a strong Phase C/D confirmation
        
        return MethodologyEvaluation(
            methodology_id=self.get_name(),
            timestamp=latest_signal.timestamp,
            is_active=is_active,
            direction=direction,
            confidence=min(1.0, confidence),
            supporting_concepts=supporting_concepts,
            metadata={"wyckoff_phase": "Phase C/D" if is_active else "Developing"}
        )
