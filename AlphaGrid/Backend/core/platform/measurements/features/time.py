from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from Backend.core.platform.measurements.engine import MeasurementEngine, Causality

class TimeFeatures(MeasurementEngine):
    """
    Emits objective temporal facts for a bar.
    Strictly causal.
    """
    measurement_type = "TimeFeatures"
    implementation_version = "1.0.0"
    causality = Causality.ONLINE
    
    def step(self, history: List[Dict[str, Any]], current_idx: int) -> Optional[Dict[str, Any]]:
        curr_bar = history[current_idx]
        ts = curr_bar["timestamp"]
        
        # Assume ts is in milliseconds
        dt = datetime.fromtimestamp(ts / 1000.0, tz=timezone.utc)
        
        return {
            "bar_index": current_idx,
            "timestamp": ts,
            "utc_hour": dt.hour,
            "utc_minute": dt.minute,
            "weekday": dt.weekday(),
            "provenance": self.get_provenance()
        }
