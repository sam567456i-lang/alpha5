from typing import List, Dict, Any, Optional
from Backend.core.platform.measurements.engine import MeasurementEngine, Causality

class CenteredPivotEngine(MeasurementEngine):
    """
    Computes standard centered pivots.
    Requires future data. Offline causality.
    """
    measurement_type = "Pivot"
    algorithm_id = "CENTERED_N_BAR"
    measurement_schema_version = "1.0.0"
    algorithm_version = "1.0.0"
    causality = Causality.OFFLINE
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.lookback = self.config.get("lookback", 5)
        self.lookforward = self.config.get("lookforward", 5)
        self.pivot_type = self.config.get("pivot_type", "HIGH") # HIGH or LOW
        
    def step(self, history: List[Dict[str, Any]], current_idx: int) -> Optional[Dict[str, Any]]:
        # A centered pivot is only evaluated when current_idx has enough lookback and lookforward
        # But wait! If this is called in BatchRunner on a full array, at current_idx we evaluate if current_idx is a pivot?
        # Or does it evaluate if current_idx - lookforward was a pivot?
        # If we evaluate if current_idx is a pivot, we need history up to current_idx + lookforward.
        # So we peek ahead.
        
        if current_idx - self.lookback < 0:
            return None
        if current_idx + self.lookforward >= len(history):
            return None
            
        center_price = history[current_idx]["high"] if self.pivot_type == "HIGH" else history[current_idx]["low"]
        
        is_pivot = True
        for j in range(current_idx - self.lookback, current_idx + self.lookforward + 1):
            if j == current_idx:
                continue
            
            comp_price = history[j]["high"] if self.pivot_type == "HIGH" else history[j]["low"]
            
            if self.pivot_type == "HIGH" and comp_price >= center_price:
                is_pivot = False
                break
            elif self.pivot_type == "LOW" and comp_price <= center_price:
                is_pivot = False
                break
                
        if is_pivot:
            return {
                "formation_bar": current_idx,
                "timestamp": history[current_idx]["timestamp"],
                "price": center_price,
                "type": self.pivot_type,
                "provenance": self.get_provenance()
            }
        return None
