import hashlib
import uuid
from typing import Dict, Any
from Backend.dtos.strategies import StrategyDTO
from Backend.dtos.signals import SignalDTO

class BollingerReversionStrategy:
    def __init__(self, bb_period: int = 20, bb_std: float = 2.0):
        self.bb_period = bb_period
        self.bb_std = bb_std
        self.component_id = "strat-bbreversion"
        
    def get_metadata(self) -> Dict[str, Any]:
        return {
            "id": self.component_id,
            "family": "Mean Reversion",
            "methodology": "meth-meanreversion",
            "required_features": [f"ftr-bollinger-{self.bb_period}-{self.bb_std}"],
            "required_geometry": [],
            "required_concepts": ["con-extremum-percent_b"],
            "required_signals": ["sig-gen-extremumreversion"],
            "supported_markets": ["Stocks", "Crypto", "Forex"],
            "supported_timeframes": ["15m", "1h", "4h", "1d"],
            "supported_styles": ["Swing", "Intraday"],
            "supported_sessions": ["ALL"],
            "minimum_history": self.bb_period * 2,
            "warmup_period": self.bb_period,
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
            
        payload = f"{action}:{self.bb_period}:{self.bb_std}"
        payload_hash = hashlib.md5(payload.encode()).hexdigest()
        
        return StrategyDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint="strat-bbreversion-base",
            checksum=payload_hash,
            action=action,
            metadata={
                "parameters_used": {
                    "bb_period": self.bb_period,
                    "bb_std": self.bb_std
                },
                "strategy_metadata": self.get_metadata()
            },
            lineage={'dependencies': [signal.id]}
        )
