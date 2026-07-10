from typing import List, Dict, Any, Optional
from Backend.core.analytical_rules.statistics_rules import VolatilityRule
from Backend.core.evidence_dtos.statistics import VolatilityEvidence

class VolatilityEngine:
    """
    Platform 10: Statistics Family - Volatility Engine.
    Orchestrates calculation of True Range, ATR, and Regimes.
    """
    
    def __init__(self):
        self.rule = VolatilityRule()
        self._atr_period = 14
        self._current_atr = 0.0
        self._count = 0
        
    def process_event(self, event: Dict[str, Any]) -> Optional[VolatilityEvidence]:
        """Processes incoming OHLCV events and emits Volatility Evidence."""
        # Update running ATR (simplified RMA)
        high = event.get("high", 0.0)
        low = event.get("low", 0.0)
        prev_close = event.get("prev_close", event.get("open", 0.0)) # Fallback if no prev_close
        
        tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
        
        if self._count == 0:
            self._current_atr = tr
        else:
            self._current_atr = (self._current_atr * (self._atr_period - 1) + tr) / self._atr_period
            
        self._count += 1
        
        market_data = {
            "asset": event.get("symbol", "UNKNOWN"),
            "timeframe": event.get("timeframe", "1m"),
            "timestamp": event.get("timestamp", 0),
            "high": high,
            "low": low,
            "prev_close": prev_close,
            "current_atr": self._current_atr
        }
        
        return self.rule.evaluate(market_data)

    def name(self) -> str:
        return "VolatilityEngine"
