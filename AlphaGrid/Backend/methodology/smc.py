"""Smart Money Concepts (SMC) Methodology."""

from typing import Dict, Any
from Backend.methodology.base import AbstractMethodology
from Backend.methodology.evaluation import MethodologyEvaluation
from Backend.signals.primitive.context import SignalContext

class SMCMethodology(AbstractMethodology):
    """
    SMC Methodology uses predefined weights to combine atomic structural primitives
    into a high-confidence trading evaluation.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        # Default Weights
        self.weights = self.config.get("weights", {
            "bos": 0.20,
            "choch": 0.25,
            "ob": 0.20,
            "liquidity": 0.20,
            "fvg": 0.15
        })

    @classmethod
    def get_name(cls) -> str:
        return "SmartMoneyConcepts"

    def evaluate(self, context: SignalContext) -> MethodologyEvaluation:
        # Retrieve the composite primitive signal emitted by MarketStructurePrimitiveGenerator
        signals = context.get_signals("MARKET_STRUCTURE_EVENT")
        if not signals:
            return MethodologyEvaluation(
                methodology_id=self.get_name(),
                timestamp=None,
                is_active=False,
                direction=0,
                confidence=0.0
            )
            
        # The latest signal contains the atomic events
        latest_signal = signals[-1]
        events = latest_signal.metadata
        
        direction = latest_signal.direction
        confidence = 0.0
        supporting_concepts = {}
        
        # Accumulate confidence based on SMC rules
        if "structure" in events:
            struct = events["structure"]
            if struct["is_bullish"] == (direction == 1):
                if struct["type"] == "BOS":
                    confidence += self.weights["bos"]
                    supporting_concepts["BOS"] = 1
                elif struct["type"] == "CHOCH":
                    confidence += self.weights["choch"]
                    supporting_concepts["CHOCH"] = 1
                    
        if events.get("ob_mitigated") and events.get("ob_bullish") == (direction == 1):
            confidence += self.weights["ob"]
            supporting_concepts["OB_MITIGATED"] = 1
            
        # Add FVG and Liquidity logic here (mocked for now)
        # confidence += self.weights["fvg"]
        # confidence += self.weights["liquidity"]

        is_active = confidence >= 0.45 # Require at least CHOCH + OB to be active
        
        return MethodologyEvaluation(
            methodology_id=self.get_name(),
            timestamp=latest_signal.timestamp,
            is_active=is_active,
            direction=direction,
            confidence=min(1.0, confidence),
            supporting_concepts=supporting_concepts,
            metadata={"source_signal": "MARKET_STRUCTURE_EVENT"}
        )
