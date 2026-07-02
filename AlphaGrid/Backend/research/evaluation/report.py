"""Scientific Evaluation Report."""

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass(frozen=True)
class ProfitabilityMetrics:
    total_return: float
    annualized_return: float
    win_rate: float
    profit_factor: float
    expectancy: float
    payoff_ratio: float

@dataclass(frozen=True)
class RiskMetrics:
    max_drawdown: float
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    var_95: float

@dataclass(frozen=True)
class RobustnessMetrics:
    walk_forward_efficiency: float
    parameter_stability: float

@dataclass(frozen=True)
class StatisticalMetrics:
    total_trades: int
    t_stat: float
    monte_carlo_survival: float

@dataclass(frozen=True)
class ScientificEvaluationReport:
    """
    Immutable report representing the final evaluation of an experiment.
    This acts as the scientific record for every backtest/walk-forward run.
    """
    experiment_id: str
    hypothesis_id: str
    profitability: Optional[ProfitabilityMetrics]
    risk: Optional[RiskMetrics]
    robustness: Optional[RobustnessMetrics]
    statistics: Optional[StatisticalMetrics]
    is_promoted: bool = False
    failure_reasons: List[str] = field(default_factory=list)
