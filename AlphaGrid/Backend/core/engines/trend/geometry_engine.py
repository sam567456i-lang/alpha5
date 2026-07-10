from typing import Dict, Any, Optional
from Backend.core.evidence_dtos.trend import TrendSlopeEvidence, TrendAccelerationEvidence

class GeometryEngine:
    """
    Platform 10: Trend Family - Geometry Engine.
    Computes objective slope and acceleration continuously.
    """
    
    def __init__(self):
        self._prev_val = None
        self._prev_slope = None
        
    def process_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Processes rolling statistics and emits Slope & Acceleration."""
        current_val = event.get("rolling_mean")
        if current_val is None:
            return {"slope": None, "acceleration": None}
            
        slope = 0.0
        accel = 0.0
        
        if self._prev_val is not None:
            # First derivative
            slope = current_val - self._prev_val
            
            if self._prev_slope is not None:
                # Second derivative
                accel = slope - self._prev_slope
                
        self._prev_val = current_val
        self._prev_slope = slope
        
        meta = {
            "asset": event.get("symbol", "UNKNOWN"),
            "timeframe": event.get("timeframe", "1m"),
            "timestamp": event.get("timestamp", 0)
        }
        
        return {
            "slope": TrendSlopeEvidence(**meta, slope=slope, slope_angle_degrees=0.0),
            "acceleration": TrendAccelerationEvidence(**meta, acceleration=accel)
        }

    def name(self) -> str:
        return "GeometryEngine"
