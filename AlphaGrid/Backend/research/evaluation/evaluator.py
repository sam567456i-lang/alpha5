"""Scientific Evaluator."""

from typing import List, Dict, Any, Optional
from Backend.research.evaluation.report import ScientificEvaluationReport
from Backend.research.evaluation.metrics import MetricsCalculator
from Backend.research.evaluation.policy import PromotionPolicy

class ScientificEvaluator:
    """
    Central orchestrator for the Scientific Evaluation Subsystem.
    Consumes experiment results (trades, equity curve) and emits an immutable ScientificEvaluationReport.
    """

    def __init__(self, policy: Optional[PromotionPolicy] = None):
        self.policy = policy or PromotionPolicy()

    def evaluate(
        self, 
        experiment_id: str, 
        hypothesis_id: str, 
        trades: List[Dict[str, Any]], 
        equity_curve: List[float],
        is_sharpe: float = 0.0,
        oos_sharpe: float = 0.0
    ) -> ScientificEvaluationReport:
        """
        Evaluate an experiment and generate a report.
        """
        
        # 1. Compute Metrics
        profitability = MetricsCalculator.calculate_profitability(trades)
        risk = MetricsCalculator.calculate_risk(equity_curve)
        statistics = MetricsCalculator.calculate_statistics(trades)
        
        # If we have Walk Forward data, compute robustness
        robustness = None
        if is_sharpe != 0.0 and oos_sharpe != 0.0:
            robustness = MetricsCalculator.calculate_robustness(is_sharpe, oos_sharpe)
            
        # 2. Build preliminary report (without promotion decision)
        report = ScientificEvaluationReport(
            experiment_id=experiment_id,
            hypothesis_id=hypothesis_id,
            profitability=profitability,
            risk=risk,
            robustness=robustness,
            statistics=statistics,
            is_promoted=False,
            failure_reasons=[]
        )
        
        # 3. Apply Policy
        is_promoted, failure_reasons = self.policy.evaluate(report)
        
        # 4. Return final immutable report
        return ScientificEvaluationReport(
            experiment_id=experiment_id,
            hypothesis_id=hypothesis_id,
            profitability=profitability,
            risk=risk,
            robustness=robustness,
            statistics=statistics,
            is_promoted=is_promoted,
            failure_reasons=failure_reasons
        )
