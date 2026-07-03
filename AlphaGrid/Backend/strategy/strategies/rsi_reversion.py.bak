import hashlib
import uuid
from typing import Dict, Any
from Backend.dtos.strategies import StrategyDTO
from Backend.dtos.signals import SignalDTO

class RSIReversionStrategy:
    def __init__(self, rsi_period: int = 14, overbought: float = 70.0, oversold: float = 30.0):
        self.rsi_period = rsi_period
        self.overbought = overbought
        self.oversold = oversold
        self.component_id = "strat-rsireversion"
        
    def get_metadata(self) -> Dict[str, Any]:
        return {
            "id": self.component_id,
            "family": "Mean Reversion",
            "methodology": "meth-meanreversion",
            "required_features": [f"ftr-rsi-{self.rsi_period}"],
            "required_geometry": [],
            "required_concepts": ["con-extremum-rsi"],
            "required_signals": ["sig-gen-extremumreversion"],
            "supported_markets": ["Stocks", "Crypto", "Forex"],
            "supported_timeframes": ["15m", "1h", "4h", "1d"],
            "supported_styles": ["Swing", "Intraday"],
            "supported_sessions": ["ALL"],
            "minimum_history": self.rsi_period * 2,
            "warmup_period": self.rsi_period,
            "version": "0.1.0"
        }
        
    def generate(self, signal: SignalDTO, trace_id: str, correlation_id: str) -> StrategyDTO:
        action = "HOLD"
        
        if signal.signal_type == "MEAN_REVERSION_LONG":
            action = "BUY"
        elif signal.signal_type == "MEAN_REVERSION_SHORT":
            action = "SELL"
        elif signal.signal_type == "MEAN_REVERSION_EXIT":
            action = "EXIT"
            
        payload = f"{action}:{self.rsi_period}:{self.overbought}:{self.oversold}"
        payload_hash = hashlib.md5(payload.encode()).hexdigest()
        
        return StrategyDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint="strat-rsireversion-base",
            checksum=payload_hash,
            action=action,
            metadata={
                "parameters_used": {
                    "rsi_period": self.rsi_period,
                    "overbought": self.overbought,
                    "oversold": self.oversold
                },
                "strategy_metadata": self.get_metadata()
            },
            lineage={'dependencies': [signal.id]}
        )
