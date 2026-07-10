from typing import List, Dict, Any, Optional
from Backend.core.platform.measurements.engine import MeasurementEngine, Causality

class TouchEngine(MeasurementEngine):
    """
    Computes interactions (Touches) between price and a reference object.
    Requires a reference object (e.g. Pivot).
    Online.
    """
    measurement_type = "Touch"
    implementation_version = "1.0.0"
    causality = Causality.ONLINE
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.reference_price = self.config.get("reference_price")
        if self.reference_price is None:
            raise ValueError("TouchEngine requires a reference_price config parameter")
            
    def step(self, history: List[Dict[str, Any]], current_idx: int) -> Optional[Dict[str, Any]]:
        current_bar = history[current_idx]
        
        # A touch occurs if the bar's high/low overlaps the reference price
        # Actually, "Touch" logic depends on direction.
        # But objectively, if low <= reference_price <= high, it touches.
        
        if current_bar["low"] <= self.reference_price <= current_bar["high"]:
            return {
                "event_type": "TOUCH",
                "bar_index": current_idx,
                "timestamp": current_bar["timestamp"],
                "observed_high": current_bar["high"],
                "observed_low": current_bar["low"],
                "reference_price": self.reference_price,
                "provenance": self.get_provenance()
            }
        return None
