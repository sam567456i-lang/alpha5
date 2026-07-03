"""MACD Trend Strategy."""

from typing import Dict, Any, List
from datetime import datetime

from Backend.strategy.objects import TradingDecision
from Backend.strategy.base import AbstractStrategy

class MACDTrendStrategy(AbstractStrategy):
    """
    MACD Trend Strategy.
    """

    STRATEGY_METADATA = {
        "Strategy ID": "MACD_TREND_V1",
        "Version": "1.0",
        "Family": "Trend Following",
        "Dependencies": ["TrendFollowingMethodology"],
        "Feature Switches": ["ENABLE_MACD_TREND"],
        "Configuration Schema": {
            "fast_ema": {"type": "int", "required": True, "default": 12},
            "slow_ema": {"type": "int", "required": True, "default": 26},
            "signal_ema": {"type": "int", "required": True, "default": 9}
        },
        "Consumes": ["MethodologyEvaluation"],
        "Produces": ["TradingDecision"],
        "Market Types": ["SPOT", "PERP"],
        "Timeframes": ["1h", "4h", "1d"]
    }

    def __init__(self, parameters: Dict[str, Any] = None):
        super().__init__(parameters)

    @classmethod
    def _get_default_parameters(cls) -> Dict[str, Any]:
        return {"fast_ema": 12, "slow_ema": 26, "signal_ema": 9}

    @classmethod
    def _get_grid_search_space(cls) -> Dict[str, List[Any]]:
        return {
            "fast_ema": [8, 12, 17],
            "slow_ema": [21, 26, 34],
            "signal_ema": [9, 14]
        }

    def evaluate(self, timestamp: datetime, methodologies: List[Any]) -> List[TradingDecision]:
        decisions = []
        for eval_obj in methodologies:
            if getattr(eval_obj, "methodology_id", "") == "TrendFollowingMethodology":
                if eval_obj.is_active and eval_obj.direction == 1:
                    decisions.append(TradingDecision(
                        strategy_id=self.STRATEGY_METADATA["Strategy ID"],
                        timestamp=timestamp,
                        action="BUY",
                        confidence=eval_obj.confidence,
                        metadata={"supporting_signals": eval_obj.metadata.get("supporting_signals", [])}
                    ))
                elif eval_obj.is_active and eval_obj.direction == -1:
                    decisions.append(TradingDecision(
                        strategy_id=self.STRATEGY_METADATA["Strategy ID"],
                        timestamp=timestamp,
                        action="SELL",
                        confidence=eval_obj.confidence,
                        metadata={"supporting_signals": eval_obj.metadata.get("supporting_signals", [])}
                    ))
        return decisions
