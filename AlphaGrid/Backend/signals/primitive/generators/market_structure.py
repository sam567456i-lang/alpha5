"""Market Structure Primitive Signal Generator."""

from typing import List, Optional
from datetime import datetime
from Backend.concepts.base import Concept
from Backend.signals.primitive.base import AbstractPrimitiveSignalGenerator, PrimitiveSignal

class MarketStructurePrimitiveGenerator(AbstractPrimitiveSignalGenerator):
    """
    Translates the atomic MarketStructureState Concept into independent Primitive Signals.
    These signals (BOS, CHOCH, Liquidity Sweep) can be consumed by any methodology (SMC, Wyckoff, ICT).
    """

    def get_id(self) -> str:
        return "MarketStructurePrimitives"
        
    def get_required_concepts(self) -> List[str]:
        return ["MarketStructureState"]
        
    def evaluate(self, timestamp: datetime, concepts: List[Concept]) -> Optional[PrimitiveSignal]:
        # This generator actually needs to emit multiple signals. 
        # But AbstractPrimitiveSignalGenerator only allows returning one Optional[PrimitiveSignal].
        # We will wrap them in a composite PrimitiveSignal or modify the engine to support lists.
        # For now, we will return a composite PrimitiveSignal whose metadata contains the atomic events.
        
        target_concept = next((c for c in concepts if c.id.startswith("MarketStructureState")), None)
        if not target_concept:
            return None
            
        state = target_concept.inputs
        events = {}
        confidence = 0.0
        direction = 0
        
        # Structure Events
        latest_structure = state.get("latest_structure")
        if latest_structure:
            events["structure"] = {
                "type": latest_structure["type"],
                "is_bullish": latest_structure["is_bullish"]
            }
            # Latest structure dictates baseline direction
            direction = 1 if latest_structure["is_bullish"] else -1
            confidence += 0.2
            
        # OB Mitigations
        obs = state.get("active_order_blocks", [])
        mitigated_obs = [ob for ob in obs if ob.get("state") == "MITIGATED"]
        if mitigated_obs:
            events["ob_mitigated"] = True
            events["ob_bullish"] = mitigated_obs[-1]["is_bullish"]
            # Align direction with most recent mitigation
            direction = 1 if mitigated_obs[-1]["is_bullish"] else -1
            confidence += 0.2
            
        # Liquidity Sweeps
        pools = state.get("active_liquidity_pools", [])
        # We assume if a pool is no longer in the active list but was, it was swept, or we track swept state.
        # For simplicity in this mock, we just pass the active pools. Real impl would diff states to find sweeps.
        events["active_pools"] = len(pools)
        
        if not events:
            return None
            
        return PrimitiveSignal(
            id="MARKET_STRUCTURE_EVENT",
            timestamp=timestamp,
            direction=direction,
            confidence=min(1.0, confidence),
            metadata=events
        )
