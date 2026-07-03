"""Feature that consumes Geometry cache to prove integration."""

from typing import Dict, Any, Optional
from Shared.models.market import MarketSnapshot
from .base import AbstractFeature

class NearestPivotDistanceFeature(AbstractFeature):
    """
    Computes the distance from the current close to the most recent pivot high/low.
    Proof that Price Geometry is actively consumed by the Feature layer.
    """
    
    @classmethod
    def get_name(cls) -> str:
        return "geom_pivot_distance"
        
    @classmethod
    def get_version(cls) -> str:
        return "v1"
        
    @classmethod
    def get_dependencies(cls) -> list[str]:
        # Requires geometry_cache to be present in the feature cache
        return ["geometry_cache"]
        
    @classmethod
    def warmup_period(cls) -> int:
        return 0
        
    def compute(self, snapshot: MarketSnapshot, cache: Dict[str, Any]) -> Optional[float]:
        # Consume geometry from cache
        geom_cache = cache.get("geometry_cache")
        if not geom_cache:
            return None
            
        pivots = geom_cache.get_by_type("Pivot")
        if not pivots:
            return None
            
        # Get the most recently formed pivot
        # Pivots have properties like 'price', 'type' (High/Low)
        latest_pivot = pivots[-1]
        
        # Calculate distance
        if hasattr(latest_pivot, "price"):
            return float(snapshot.close) - float(latest_pivot.price)
        return 0.0
