from typing import List, Dict, Any, Optional
from Backend.core.platform.measurements.engine import MeasurementEngine, Causality

class Highest(MeasurementEngine):
    measurement_type = "Highest"
    implementation_version = "1.0.0"
    causality = Causality.ONLINE
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.period = self.config.get("period", 20)
        self.source = self.config.get("source", "high")
        
    def step(self, history: List[Dict[str, Any]], current_idx: int) -> Optional[Dict[str, Any]]:
        if current_idx < self.period - 1:
            return None
            
        vals = [history[i][self.source] for i in range(current_idx - self.period + 1, current_idx + 1)]
        
        return {
            "bar_index": current_idx,
            "timestamp": history[current_idx]["timestamp"],
            "value": max(vals),
            "provenance": self.get_provenance()
        }

class Lowest(MeasurementEngine):
    measurement_type = "Lowest"
    implementation_version = "1.0.0"
    causality = Causality.ONLINE
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.period = self.config.get("period", 20)
        self.source = self.config.get("source", "low")
        
    def step(self, history: List[Dict[str, Any]], current_idx: int) -> Optional[Dict[str, Any]]:
        if current_idx < self.period - 1:
            return None
            
        vals = [history[i][self.source] for i in range(current_idx - self.period + 1, current_idx + 1)]
        
        return {
            "bar_index": current_idx,
            "timestamp": history[current_idx]["timestamp"],
            "value": min(vals),
            "provenance": self.get_provenance()
        }

class Range(MeasurementEngine):
    measurement_type = "Range"
    implementation_version = "1.0.0"
    causality = Causality.ONLINE
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.period = self.config.get("period", 20)
        
    def step(self, history: List[Dict[str, Any]], current_idx: int) -> Optional[Dict[str, Any]]:
        if current_idx < self.period - 1:
            return None
            
        highs = [history[i]["high"] for i in range(current_idx - self.period + 1, current_idx + 1)]
        lows = [history[i]["low"] for i in range(current_idx - self.period + 1, current_idx + 1)]
        
        return {
            "bar_index": current_idx,
            "timestamp": history[current_idx]["timestamp"],
            "value": max(highs) - min(lows),
            "provenance": self.get_provenance()
        }
