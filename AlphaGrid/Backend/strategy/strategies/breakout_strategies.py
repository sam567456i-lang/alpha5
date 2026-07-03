import hashlib
import uuid
from typing import Dict, Any
from Backend.dtos.strategies import StrategyDTO
from Backend.dtos.signals import SignalDTO


class SRBreakoutStrategy:
    """Support/Resistance Breakout Strategy."""

    def __init__(self, sr_lookback: int = 20):
        self.sr_lookback = sr_lookback
        self.component_id = "strat-srbreakout"

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "id": self.component_id,
            "family": "Breakout",
            "methodology": "meth-breakout",
            "required_features": [f"ftr-sr-{self.sr_lookback}"],
            "required_geometry": [],
            "required_concepts": ["con-breakout"],
            "required_methodologies": ["meth-breakout"],
            "required_signals": ["sig-gen-breakout"],
            "supported_markets": ["Stocks", "Crypto", "Forex", "Futures"],
            "supported_timeframes": ["15m", "1h", "4h", "1d"],
            "supported_styles": ["Intraday", "Swing"],
            "supported_sessions": ["ALL"],
            "minimum_history": self.sr_lookback * 2,
            "warmup_period": self.sr_lookback,
            "parameter_space_version": "1.0.0",
            "strategy_version": "0.1.0",
            "version": "0.1.0",
        }

    def generate(self, signal: SignalDTO, trace_id: str, correlation_id: str) -> StrategyDTO:
        action = "HOLD"
        if "LONG" in signal.signal_type:
            action = "BUY"
        elif "SHORT" in signal.signal_type:
            action = "SELL"

        payload = f"{action}:{self.sr_lookback}"
        payload_hash = hashlib.md5(payload.encode()).hexdigest()

        return StrategyDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint="strat-srbreakout-base",
            checksum=payload_hash,
            action=action,
            metadata={
                "parameters_used": {"sr_lookback": self.sr_lookback},
                "strategy_metadata": self.get_metadata(),
            },
            lineage={'dependencies': [signal.id]}
        )


class HighLowBreakoutStrategy:
    """N-Period High/Low Breakout Strategy."""

    def __init__(self, period: int = 20):
        self.period = period
        self.component_id = "strat-hlbreakout"

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "id": self.component_id,
            "family": "Breakout",
            "methodology": "meth-breakout",
            "required_features": [f"ftr-hlbreakout-{self.period}"],
            "required_geometry": [],
            "required_concepts": ["con-breakout"],
            "required_methodologies": ["meth-breakout"],
            "required_signals": ["sig-gen-breakout"],
            "supported_markets": ["Stocks", "Crypto", "Forex", "Futures"],
            "supported_timeframes": ["1h", "4h", "1d"],
            "supported_styles": ["Swing", "Position"],
            "supported_sessions": ["ALL"],
            "minimum_history": self.period * 2,
            "warmup_period": self.period,
            "parameter_space_version": "1.0.0",
            "strategy_version": "0.1.0",
            "version": "0.1.0",
        }

    def generate(self, signal: SignalDTO, trace_id: str, correlation_id: str) -> StrategyDTO:
        action = "HOLD"
        if "LONG" in signal.signal_type:
            action = "BUY"
        elif "SHORT" in signal.signal_type:
            action = "SELL"

        payload = f"{action}:{self.period}"
        payload_hash = hashlib.md5(payload.encode()).hexdigest()

        return StrategyDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint="strat-hlbreakout-base",
            checksum=payload_hash,
            action=action,
            metadata={
                "parameters_used": {"period": self.period},
                "strategy_metadata": self.get_metadata(),
            },
            lineage={'dependencies': [signal.id]}
        )


class VolatilityBreakoutStrategy:
    """ATR-Based Volatility Breakout Strategy."""

    def __init__(self, atr_period: int = 14, multiplier: float = 1.5):
        self.atr_period = atr_period
        self.multiplier = multiplier
        self.component_id = "strat-volbreakout"

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "id": self.component_id,
            "family": "Breakout",
            "methodology": "meth-breakout",
            "required_features": [f"ftr-volbreakout-{self.atr_period}-{self.multiplier}"],
            "required_geometry": [],
            "required_concepts": ["con-breakout"],
            "required_methodologies": ["meth-breakout"],
            "required_signals": ["sig-gen-breakout"],
            "supported_markets": ["Stocks", "Crypto", "Forex", "Futures"],
            "supported_timeframes": ["15m", "1h", "4h"],
            "supported_styles": ["Scalping", "Intraday"],
            "supported_sessions": ["ALL"],
            "minimum_history": self.atr_period * 3,
            "warmup_period": self.atr_period,
            "parameter_space_version": "1.0.0",
            "strategy_version": "0.1.0",
            "version": "0.1.0",
        }

    def generate(self, signal: SignalDTO, trace_id: str, correlation_id: str) -> StrategyDTO:
        action = "HOLD"
        if "LONG" in signal.signal_type:
            action = "BUY"
        elif "SHORT" in signal.signal_type:
            action = "SELL"

        payload = f"{action}:{self.atr_period}:{self.multiplier}"
        payload_hash = hashlib.md5(payload.encode()).hexdigest()

        return StrategyDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint="strat-volbreakout-base",
            checksum=payload_hash,
            action=action,
            metadata={
                "parameters_used": {
                    "atr_period": self.atr_period,
                    "multiplier": self.multiplier,
                },
                "strategy_metadata": self.get_metadata(),
            },
            lineage={'dependencies': [signal.id]}
        )
