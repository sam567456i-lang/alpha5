from typing import List, Dict, Any, Optional
from Backend.core.platform.measurements.engine import MeasurementEngine, Causality

class BarEngine(MeasurementEngine):
    """
    Pass-through object engine for raw OHLC bars.
    Strictly causal.
    """
    measurement_type = "Bar"
    implementation_version = "1.0.0"
    causality = Causality.ONLINE
    
    def step(self, history: List[Dict[str, Any]], current_idx: int) -> Optional[Dict[str, Any]]:
        if current_idx < 0 or current_idx >= len(history):
            return None
        
        raw_bar = history[current_idx]
        return {
            "bar_index": current_idx,
            "timestamp": raw_bar["timestamp"],
            "open": raw_bar["open"],
            "high": raw_bar["high"],
            "low": raw_bar["low"],
            "close": raw_bar["close"],
            "provenance": self.get_provenance()
        }
