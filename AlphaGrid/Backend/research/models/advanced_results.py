"""Result models for advanced research engines."""

from typing import Any, Dict, List
from uuid import UUID
from datetime import datetime

from Shared.models.common import AlphaGridBaseModel


class WalkForwardFold(AlphaGridBaseModel):
    """Stores independent data for a single walk-forward fold."""
    fold_number: int
    is_start: datetime
    is_end: datetime
    oos_start: datetime
    oos_end: datetime
    is_metrics: Dict[str, Any]
    oos_metrics: Dict[str, Any]


class WalkForwardResult(AlphaGridBaseModel):
    """Aggregated output from a walk-forward optimization run."""
    experiment_id: UUID
    folds: List[WalkForwardFold]
    aggregated_metrics: Dict[str, Any]


class MonteCarloIteration(AlphaGridBaseModel):
    """Stores independent data for a single Monte Carlo simulation iteration."""
    iteration_number: int
    seed: int
    parameters: Dict[str, Any]
    metrics: Dict[str, Any]


class MonteCarloResult(AlphaGridBaseModel):
    """Aggregated distribution metrics for a Monte Carlo simulation run."""
    experiment_id: UUID
    iterations: List[MonteCarloIteration]
    distribution_metrics: Dict[str, Any]
