"""Promotion Policy."""

from dataclasses import dataclass
from typing import List, Tuple
from Backend.research.evaluation.report import ScientificEvaluationReport

@dataclass
class PromotionPolicy:
    """Declarative thresholds for promoting an experiment to the Candidate Registry."""
    min_trades: int = 30
    min_profit_factor: float = 1.2
    min_sharpe: float = 0.5
    max_drawdown: float = 0.20
    min_wfe: float = 0.5
    min_t_stat: float = 1.96

    def evaluate(self, report: ScientificEvaluationReport) -> Tuple[bool, List[str]]:
        """
        Evaluates the report against this policy.
        Returns (is_promoted, list_of_failure_reasons).
        """
        failures = []
        
        # Statistical
        if not report.statistics or report.statistics.total_trades < self.min_trades:
            failures.append(f"Insufficient trades: {report.statistics.total_trades if report.statistics else 0} < {self.min_trades}")
        if report.statistics and report.statistics.t_stat < self.min_t_stat:
            failures.append(f"T-Stat too low: {report.statistics.t_stat:.2f} < {self.min_t_stat}")
            
        # Profitability
        if not report.profitability or report.profitability.profit_factor < self.min_profit_factor:
            pf = report.profitability.profit_factor if report.profitability else 0.0
            failures.append(f"Profit factor too low: {pf:.2f} < {self.min_profit_factor}")
            
        # Risk
        if not report.risk or report.risk.sharpe_ratio < self.min_sharpe:
            sr = report.risk.sharpe_ratio if report.risk else 0.0
            failures.append(f"Sharpe ratio too low: {sr:.2f} < {self.min_sharpe}")
            
        if report.risk and report.risk.max_drawdown > self.max_drawdown:
            failures.append(f"Drawdown too high: {report.risk.max_drawdown:.2f} > {self.max_drawdown}")
            
        # Robustness
        if report.robustness and report.robustness.walk_forward_efficiency < self.min_wfe:
            failures.append(f"WFE too low: {report.robustness.walk_forward_efficiency:.2f} < {self.min_wfe}")
            
        return len(failures) == 0, failures
