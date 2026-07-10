from typing import List, Dict, Any, Optional
import math
from Backend.core.platform.measurements.engine import MeasurementEngine, Causality

class ATR(MeasurementEngine):
    """
    Computes Average True Range over a specified period.
    Online causality.
    """
    measurement_type = "ATR"
    implementation_version = "1.0.0"
    causality = Causality.ONLINE
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.period = self.config.get("period", 14)
        
    def step(self, history: List[Dict[str, Any]], current_idx: int) -> Optional[Dict[str, Any]]:
        if current_idx < self.period:
            return None
            
        trs = []
        for i in range(current_idx - self.period + 1, current_idx + 1):
            curr = history[i]
            if i == 0:
                tr = curr["high"] - curr["low"]
            else:
                prev = history[i-1]
                hl = curr["high"] - curr["low"]
                hc = abs(curr["high"] - prev["close"])
                lc = abs(curr["low"] - prev["close"])
                tr = max(hl, hc, lc)
            trs.append(tr)
            
        atr_val = sum(trs) / self.period
        
        return {
            "bar_index": current_idx,
            "timestamp": history[current_idx]["timestamp"],
            "value": atr_val,
            "period": self.period,
            "provenance": self.get_provenance()
        }

class RealizedVolatility(MeasurementEngine):
    """
    Computes annualized realized volatility of log returns.
    Online causality.
    """
    measurement_type = "RealizedVolatility"
    implementation_version = "1.0.0"
    causality = Causality.ONLINE
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.period = self.config.get("period", 21)
        self.annualization_factor = self.config.get("annualization_factor", 365 * 24) # Default 1H crypto
        
    def step(self, history: List[Dict[str, Any]], current_idx: int) -> Optional[Dict[str, Any]]:
        if current_idx < self.period:
            return None
            
        log_returns = []
        for i in range(current_idx - self.period + 1, current_idx + 1):
            if i == 0:
                continue
            curr_c = history[i]["close"]
            prev_c = history[i-1]["close"]
            if prev_c <= 0 or curr_c <= 0:
                continue
            log_returns.append(math.log(curr_c / prev_c))
            
        if not log_returns:
            return None
            
        mean_ret = sum(log_returns) / len(log_returns)
        var = sum((r - mean_ret)**2 for r in log_returns) / (len(log_returns) - 1) if len(log_returns) > 1 else 0
        std = math.sqrt(var)
        rv = std * math.sqrt(self.annualization_factor)
        
        return {
            "bar_index": current_idx,
            "timestamp": history[current_idx]["timestamp"],
            "value": rv,
            "period": self.period,
            "provenance": self.get_provenance()
        }
