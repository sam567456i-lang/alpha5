from typing import List, Dict, Any, Optional
import math
from Backend.core.platform.measurements.engine import MeasurementEngine, Causality

class RollingMean(MeasurementEngine):
    measurement_type = "RollingMean"
    implementation_version = "1.0.0"
    causality = Causality.ONLINE
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.period = self.config.get("period", 20)
        self.source = self.config.get("source", "close")
        
    def step(self, history: List[Dict[str, Any]], current_idx: int) -> Optional[Dict[str, Any]]:
        if current_idx < self.period - 1:
            return None
            
        vals = [history[i][self.source] for i in range(current_idx - self.period + 1, current_idx + 1)]
        mean = sum(vals) / self.period
        
        return {
            "bar_index": current_idx,
            "timestamp": history[current_idx]["timestamp"],
            "value": mean,
            "provenance": self.get_provenance()
        }

class RollingStdDev(MeasurementEngine):
    measurement_type = "RollingStdDev"
    implementation_version = "1.0.0"
    causality = Causality.ONLINE
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.period = self.config.get("period", 20)
        self.source = self.config.get("source", "close")
        
    def step(self, history: List[Dict[str, Any]], current_idx: int) -> Optional[Dict[str, Any]]:
        if current_idx < self.period - 1:
            return None
            
        vals = [history[i][self.source] for i in range(current_idx - self.period + 1, current_idx + 1)]
        mean = sum(vals) / self.period
        var = sum((v - mean)**2 for v in vals) / (self.period - 1) if self.period > 1 else 0
        std = math.sqrt(var)
        
        return {
            "bar_index": current_idx,
            "timestamp": history[current_idx]["timestamp"],
            "value": std,
            "provenance": self.get_provenance()
        }
