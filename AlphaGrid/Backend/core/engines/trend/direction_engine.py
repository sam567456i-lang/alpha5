from typing import Dict, Any, Optional
from Backend.core.analytical_rules.trend_rules import TrendDirectionRule
from Backend.core.evidence_dtos.trend import TrendDirectionEvidence

class DirectionEngine:
    """
    Platform 10: Trend Family - Direction Engine.
    Emits objective direction based on raw geometry evidence.
    """
    
    def __init__(self):
        self.rule = TrendDirectionRule()
        # In a real engine, threshold logic would adapt dynamically via VolatilityEvidence
        self._slope_threshold = 0.005 
        
    def process_event(self, event: Dict[str, Any]) -> Optional[TrendDirectionEvidence]:
        slope = event.get("slope")
        if slope is None:
            return None
            
        meta = {
            "asset": event.get("symbol", "UNKNOWN"),
            "timeframe": event.get("timeframe", "1m"),
            "timestamp": event.get("timestamp", 0)
        }
        
        return self.rule.evaluate(slope, self._slope_threshold, meta)

    def name(self) -> str:
        return "DirectionEngine"
