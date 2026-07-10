from typing import Dict, Any, Optional
from Backend.core.evidence_dtos.geometry import DistanceEvidence
from Backend.core.evidence_dtos.swing import PivotEvidence
from Backend.core.analytical_rules.geometry_rules import GeometryDistanceRule

class DistanceEngine:
    """
    Platform 10: Geometry Family - Distance Engine.
    Computes spatial distances between objects.
    """
    def __init__(self):
        self.rule = GeometryDistanceRule()
        
    def process_event(self, pivot_a: Dict[str, Any], pivot_b: Dict[str, Any], atr: float, tick_size: float = 0.01) -> Optional[DistanceEvidence]:
        p_a = PivotEvidence(
            asset=pivot_a.get("asset", "UNKNOWN"),
            timeframe=pivot_a.get("timeframe", "1m"),
            timestamp=pivot_a.get("timestamp", 0),
            pivot_type=pivot_a.get("pivot_type", "High"),
            price=pivot_a.get("price", 0.0)
        )
        
        p_b = PivotEvidence(
            asset=pivot_b.get("asset", "UNKNOWN"),
            timeframe=pivot_b.get("timeframe", "1m"),
            timestamp=pivot_b.get("timestamp", 0),
            pivot_type=pivot_b.get("pivot_type", "High"),
            price=pivot_b.get("price", 0.0)
        )
        
        return self.rule.evaluate(p_a, p_b, atr, tick_size)

    def name(self) -> str:
        return "DistanceEngine"
