"""MACD Momentum Strategy (Canonical Runtime)."""

from typing import Dict, Any, List
from datetime import datetime

from Backend.strategy.objects import TradingDecision
from Backend.strategy.base import AbstractStrategy
from Backend.dtos.signals import SignalDTO

class MACDMomentumStrategy(AbstractStrategy):
    """
    Canonical Runtime MACD Momentum Strategy.
    """

    STRATEGY_METADATA = {
        "Strategy ID": "MACD_MOMENTUM_RUNTIME",
        "Version": "1.0",
        "Family": "Momentum",
        "Dependencies": ["MomentumRuntimeSignalGenerator"],
        "Feature Switches": ["ENABLE_MACD_MOMENTUM"],
        "Configuration Schema": {
            "fast_ema": {"type": "int", "required": True, "default": 12},
            "slow_ema": {"type": "int", "required": True, "default": 26},
            "signal_ema": {"type": "int", "required": True, "default": 9}
        },
        "Consumes": ["SignalDTO"],
        "Produces": ["TradingDecision"],
        "required_features": ["ftr-macd"],
        "optional_features": [],
        "required_concepts": ["con-momentum-semantic"],
        "optional_concepts": [],
        "required_methodologies": ["meth-momentum-runtime"],
        "optional_methodologies": [],
        "supported_markets": ["SPOT", "PERP", "FUTURES"],
        "supported_sessions": ["24/7", "RTH"],
        "supported_timeframes": ["15m", "1h", "4h", "1d"],
        "supported_assets": ["CRYPTO", "EQUITIES", "FOREX"],
        "warmup": 35,
        "complexity": "O(1)",
        "latency_class": "low_latency",
        "risk_profile": "medium",
        "research_status": "planned",
        "freeze_status": "not_started",
        "failure_modes": {
            "Expected": ["Missing Data", "Stale Feature Data"],
            "Unexpected": ["Corrupted Signal Payload", "Invalid Direction"],
            "Recovery": ["Skip Bar", "Invalidate Active Positions"],
            "Retry": ["None - Real-time system"],
            "Fatal": ["NaNs in feature output"]
        }
    }

    def __init__(self, parameters: Dict[str, Any] = None):
        super().__init__(parameters)

    @classmethod
    def _get_default_parameters(cls) -> Dict[str, Any]:
        return {"fast_ema": 12, "slow_ema": 26, "signal_ema": 9}

    @classmethod
    def _get_grid_search_space(cls) -> Dict[str, List[Any]]:
        return {
            "fast_ema": [8, 12],
            "slow_ema": [21, 26],
            "signal_ema": [9]
        }

    def evaluate(self, timestamp: datetime, signals: List[SignalDTO]) -> List[TradingDecision]:
        decisions = []
        for sig in signals:
            if "momentum-runtime" in sig.producer:
                if sig.signal_type == "ENTRY_READY":
                    action = "BUY" if sig.direction == 1 else "SELL"
                    decisions.append(TradingDecision(
                        strategy_id=self.STRATEGY_METADATA["Strategy ID"],
                        timestamp=timestamp,
                        action=action,
                        confidence=sig.metadata.get("confidence", 0.5),
                        metadata={"signal_id": sig.id, "priority": sig.metadata.get("priority")}
                    ))
                elif sig.signal_type == "WEAKENING":
                    action = "EXIT_LONG" if sig.direction == 1 else "EXIT_SHORT"
                    decisions.append(TradingDecision(
                        strategy_id=self.STRATEGY_METADATA["Strategy ID"],
                        timestamp=timestamp,
                        action=action,
                        confidence=sig.metadata.get("confidence", 0.5),
                        metadata={"signal_id": sig.id, "reason": "Momentum Exhaustion"}
                    ))
        return decisions
