"""EMA Cross Strategy."""

from typing import Dict, Any, List
from datetime import datetime

from Backend.strategy.objects import TradingDecision
from Backend.strategy.base import AbstractStrategy

class EMACrossStrategy(AbstractStrategy):
    """
    EMA Cross Strategy.
    Evaluates the TrendFollowingMethodology output and makes a TradingDecision.
    """

    # Static Strategy Metadata (Rule 15.1)
    STRATEGY_METADATA = {
        "Strategy ID": "EMA_CROSS_V1",
        "Version": "1.0",
        "Family": "Trend Following",
        "Dependencies": ["TrendFollowingMethodology"],
        "Feature Switches": ["ENABLE_EMA_CROSS"],
        "Configuration Schema": {
            "fast_period": {"type": "int", "required": True, "default": 20},
            "slow_period": {"type": "int", "required": True, "default": 50},
        },
        "Consumes": ["MethodologyEvaluation"],
        "Produces": ["TradingDecision"],
        "Market Types": ["SPOT", "PERP"],
        "Timeframes": ["1h", "4h", "1d"]
    }

    def __init__(self, parameters: Dict[str, Any] = None):
        super().__init__(parameters)
        self.fast_period = self.parameters.get("fast_period", 20)
        self.slow_period = self.parameters.get("slow_period", 50)

    @classmethod
    def _get_default_parameters(cls) -> Dict[str, Any]:
        return {"fast_period": 20, "slow_period": 50}

    @classmethod
    def _get_grid_search_space(cls) -> Dict[str, List[Any]]:
        return {
            "fast_period": [10, 20, 50],
            "slow_period": [50, 100, 200]
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
