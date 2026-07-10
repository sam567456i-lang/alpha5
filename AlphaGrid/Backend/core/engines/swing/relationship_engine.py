from typing import Dict, Any, Optional
from Backend.core.evidence_dtos.swing import PivotEvidence, SwingRelationshipEvidence
from Backend.core.analytical_rules.swing_rules import SwingRelationshipRule

class RelationshipEngine:
    """
    Platform 10: Swing Family - Relationship Engine.
    Maps current confirmed pivot to previous confirmed pivot of the same type.
    """
    def __init__(self):
        self.rule = SwingRelationshipRule()
        self.last_high: Optional[PivotEvidence] = None
        self.last_low: Optional[PivotEvidence] = None
        
    def process_event(self, event: Dict[str, Any]) -> Optional[SwingRelationshipEvidence]:
        # Expects PivotLifecycleEvidence, but we just need it to be "Confirmed" or "Active"
        if event.get("state") not in ["Confirmed", "Active"]:
            return None
            
        pivot_type = event.get("pivot_type")
        current_pivot = PivotEvidence(
            asset=event.get("asset", "UNKNOWN"),
            timeframe=event.get("timeframe", "1m"),
            timestamp=event.get("timestamp", 0),
            pivot_type=pivot_type,
            price=event.get("price", 0.0)
        )
        
        rel_evidence = None
        atr = event.get("atr", 1.0) # From StatisticsEvidence (mocked via event here)
        
        if pivot_type == "High":
            if self.last_high is not None:
                rel_evidence = self.rule.evaluate(current_pivot, self.last_high, atr)
            self.last_high = current_pivot
        elif pivot_type == "Low":
            if self.last_low is not None:
                rel_evidence = self.rule.evaluate(current_pivot, self.last_low, atr)
            self.last_low = current_pivot
            
        return rel_evidence

    def name(self) -> str:
        return "RelationshipEngine"
