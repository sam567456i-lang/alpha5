import math
from typing import Dict, Any, Optional
from Backend.core.evidence_dtos.geometry import (
    DistanceEvidence,
    VectorEvidence,
    IntersectionEvidence,
    ContainmentEvidence
)
from Backend.core.evidence_dtos.swing import PivotEvidence
from Backend.core.evidence_dtos.range import RangeBoundaryEvidence

class GeometryDistanceRule:
    """Computes spatial distances between objects."""
    
    def evaluate(self, point_a: PivotEvidence, point_b: PivotEvidence, atr: float, tick_size: float = 0.01) -> DistanceEvidence:
        dp = abs(point_a.price - point_b.price)
        dt = abs(point_a.timestamp - point_b.timestamp)
        
        return DistanceEvidence(
            asset=point_a.asset,
            timeframe=point_a.timeframe,
            timestamp=max(point_a.timestamp, point_b.timestamp),
            distance_price=dp,
            distance_time=dt,
            distance_ticks=dp / tick_size if tick_size > 0 else 0.0,
            distance_atr=dp / atr if atr > 0 else 0.0
        )

class GeometryVectorRule:
    """Computes vectors and slopes."""
    
    def evaluate(self, point_a: PivotEvidence, point_b: PivotEvidence) -> VectorEvidence:
        dp = point_b.price - point_a.price
        dt = point_b.timestamp - point_a.timestamp
        
        # Stability: Handle vertical slope
        slope = float('inf') if dt == 0 else dp / dt
        
        # Angle in degrees
        angle = math.degrees(math.atan(slope)) if dt != 0 else (90.0 if dp > 0 else -90.0)
        
        return VectorEvidence(
            asset=point_b.asset,
            timeframe=point_b.timeframe,
            timestamp=point_b.timestamp,
            slope=slope,
            angle_degrees=angle,
            vector_dp=dp,
            vector_dt=dt
        )

class GeometryContainmentRule:
    """Computes whether a point is contained within a range."""
    
    def evaluate(self, price: float, timestamp: int, container: RangeBoundaryEvidence) -> ContainmentEvidence:
        is_contained = (price <= container.range_high) and (price >= container.range_low)
        
        width = container.range_high - container.range_low
        if width == 0:
            pct = 1.0 if price == container.range_high else 0.0
        else:
            pct = (price - container.range_low) / width
            
        return ContainmentEvidence(
            asset=container.asset,
            timeframe=container.timeframe,
            timestamp=timestamp,
            is_contained=is_contained,
            containment_percentage=pct,
            container_object_type="RangeBoundary"
        )
