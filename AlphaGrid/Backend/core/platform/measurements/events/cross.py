from typing import List, Dict, Any, Optional
from Backend.core.platform.measurements.engine import MeasurementEngine, Causality

class CrossEngine(MeasurementEngine):
    """
    Computes CrossEvents. 
    A CrossEvent happens when price fully traverses the reference price (e.g. close above/below).
    Online.
    """
    measurement_type = "Cross"
    implementation_version = "1.0.0"
    causality = Causality.ONLINE
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.reference_price = self.config.get("reference_price")
        if self.reference_price is None:
            raise ValueError("CrossEngine requires a reference_price config parameter")
            
    def step(self, history: List[Dict[str, Any]], current_idx: int) -> Optional[Dict[str, Any]]:
        if current_idx == 0:
            return None
            
        curr_bar = history[current_idx]
        prev_bar = history[current_idx - 1]
        
        # Cross UP: prev close below reference, curr close above reference
        crossed_up = prev_bar["close"] <= self.reference_price < curr_bar["close"]
        # Cross DOWN: prev close above reference, curr close below reference
        crossed_down = prev_bar["close"] >= self.reference_price > curr_bar["close"]
        
        if crossed_up or crossed_down:
            return {
                "event_type": "CROSS",
                "direction": "UP" if crossed_up else "DOWN",
                "previous_relation": "BELOW" if crossed_up else "ABOVE",
                "current_relation": "ABOVE" if crossed_up else "BELOW",
                "bar_index": current_idx,
                "timestamp": curr_bar["timestamp"],
                "observed_price": curr_bar["close"],
                "reference_price": self.reference_price,
                "provenance": self.get_provenance()
            }
            
        return None
