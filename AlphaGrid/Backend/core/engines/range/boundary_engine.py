from typing import Dict, Any, Optional
from Backend.core.evidence_dtos.range import RangeBoundaryEvidence
from Backend.core.evidence_dtos.swing import PivotEvidence
from Backend.core.analytical_rules.range_rules import RangeBoundaryRule

class BoundaryEngine:
    """
    Platform 10: Range Family - Boundary Engine.
    Consumes PivotEvidence to emit RangeBoundaryEvidence.
    """
    def __init__(self):
        self.rule = RangeBoundaryRule()
        self.last_pivot: Optional[PivotEvidence] = None
        
    def process_event(self, pivot_event: Dict[str, Any]) -> Optional[RangeBoundaryEvidence]:
        # pivot_event should simulate a Confirmed PivotLifecycleEvidence
        if pivot_event.get("state") != "Confirmed":
            return None
            
        current_pivot = PivotEvidence(
            asset=pivot_event.get("asset", "UNKNOWN"),
            timeframe=pivot_event.get("timeframe", "1m"),
            timestamp=pivot_event.get("timestamp", 0),
            pivot_type=pivot_event.get("pivot_type", "High"),
            price=pivot_event.get("price", 0.0)
        )
        
        boundary = None
        if self.last_pivot is not None:
            # We only form a range boundary if pivots are alternating types
            if self.last_pivot.pivot_type != current_pivot.pivot_type:
                boundary = self.rule.evaluate(self.last_pivot, current_pivot)
                
        self.last_pivot = current_pivot
        return boundary

    def name(self) -> str:
        return "BoundaryEngine"
