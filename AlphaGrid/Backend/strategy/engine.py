"""Strategy Engine.

Executes strategies that consume MethodologyEvaluations and generate Trading Decisions.
"""

from typing import List, Any
import logging

logger = logging.getLogger(__name__)

class StrategyEngine:
    """
    Evaluates Strategy rules against Methodology outputs.
    """

    ENGINE_METADATA = {
        "owner": "Strategy Domain",
        "version": "1.0.0",
        "consumes": "MethodologyEvaluation",
        "produces": "Decision",
        "registry": "strategy_registry",
        "contract_version": "v1",
        "downstream": "EvidenceEngine" # Next step in pipeline after Strategy/Research
    }

    def __init__(self) -> None:
        # Hardcoding the EMA strategy for Cycle 1 validation. 
        # In the future this should be dynamically loaded via strategy_registry.
        from Backend.strategy.strategies.ema_cross import EMACrossStrategy
        self.strategies = [EMACrossStrategy()]

    def process(self, timestamp: Any, evaluations: List[Any]) -> List[Any]:
        """
        Processes MethodologyEvaluations into Decisions.
        """
        decisions = []
        # Support both single evaluation and list of evaluations
        if not isinstance(evaluations, list):
            evaluations = [evaluations]
            
        for strategy in self.strategies:
            strat_decisions = strategy.evaluate(timestamp, evaluations)
            decisions.extend(strat_decisions)
            
        return decisions
