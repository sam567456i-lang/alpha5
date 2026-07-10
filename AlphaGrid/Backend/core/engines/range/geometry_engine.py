from typing import Dict, Any, Optional
from Backend.core.evidence_dtos.range import RangeBoundaryEvidence, RangeGeometryEvidence
from Backend.core.analytical_rules.range_rules import RangeGeometryRule

class GeometryEngine:
    """
    Platform 10: Range Family - Geometry Engine.
    Consumes RangeBoundaryEvidence and computes scalar properties.
    """
    def __init__(self):
        self.rule = RangeGeometryRule()
        
    def process_event(self, boundary_event: Dict[str, Any], current_timestamp: int, tick_size: float = 0.01) -> RangeGeometryEvidence:
        boundary = RangeBoundaryEvidence(
            asset=boundary_event.get("asset", "UNKNOWN"),
            timeframe=boundary_event.get("timeframe", "1m"),
            timestamp=boundary_event.get("timestamp", 0),
            range_high=boundary_event.get("range_high", 0.0),
            range_low=boundary_event.get("range_low", 0.0),
            midpoint=boundary_event.get("midpoint", 0.0),
            origin_timestamp=boundary_event.get("origin_timestamp", 0)
        )
        
        return self.rule.evaluate(boundary, current_timestamp, tick_size)

    def name(self) -> str:
        return "GeometryEngine"
