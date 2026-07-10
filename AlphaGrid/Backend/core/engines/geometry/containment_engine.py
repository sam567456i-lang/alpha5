from typing import Dict, Any, Optional
from Backend.core.evidence_dtos.geometry import ContainmentEvidence
from Backend.core.evidence_dtos.range import RangeBoundaryEvidence
from Backend.core.analytical_rules.geometry_rules import GeometryContainmentRule

class ContainmentEngine:
    """
    Platform 10: Geometry Family - Containment Engine.
    Computes containment of points inside a range.
    """
    def __init__(self):
        self.rule = GeometryContainmentRule()
        
    def process_event(self, price: float, timestamp: int, range_boundary: Dict[str, Any]) -> ContainmentEvidence:
        boundary = RangeBoundaryEvidence(
            asset=range_boundary.get("asset", "UNKNOWN"),
            timeframe=range_boundary.get("timeframe", "1m"),
            timestamp=range_boundary.get("timestamp", 0),
            range_high=range_boundary.get("range_high", 0.0),
            range_low=range_boundary.get("range_low", 0.0),
            midpoint=range_boundary.get("midpoint", 0.0),
            origin_timestamp=range_boundary.get("origin_timestamp", 0)
        )
        
        return self.rule.evaluate(price, timestamp, boundary)

    def name(self) -> str:
        return "ContainmentEngine"
