from typing import List, Dict, Any, Optional
from Backend.core.analytical_rules.statistics_rules import DistributionRule
from Backend.core.evidence_dtos.statistics import DistributionEvidence

class DistributionEngine:
    """
    Platform 10: Statistics Family - Distribution Engine.
    Orchestrates streaming calculation of distribution metrics.
    """
    
    def __init__(self):
        super().__init__()
        self.rule = DistributionRule()
        # In a real O(1) streaming engine, we'd keep Welford's running totals here
        self._price_buffer: List[float] = []
        self._max_buffer = 100
        
    def process_event(self, event: Dict[str, Any]) -> Optional[DistributionEvidence]:
        """Processes incoming OHLCV events and emits Distribution Evidence."""
        close_price = event.get("close")
        if close_price is not None:
            self._price_buffer.append(close_price)
            if len(self._price_buffer) > self._max_buffer:
                self._price_buffer.pop(0)
                
        # Only compute if we have enough data
        if len(self._price_buffer) < 2:
            return None
            
        market_data = {
            "asset": event.get("symbol", "UNKNOWN"),
            "timeframe": event.get("timeframe", "1m"),
            "timestamp": event.get("timestamp", 0),
            "closes": self._price_buffer
        }
        
        return self.rule.evaluate(market_data)

    def name(self) -> str:
        return "DistributionEngine"
