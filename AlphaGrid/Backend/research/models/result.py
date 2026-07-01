"""Backtest result model for the Research Platform."""

from typing import Any, Dict, List
from uuid import UUID
from pydantic import Field
from Shared.models.common import AlphaGridBaseModel


class BacktestResult(AlphaGridBaseModel):
    """Stores the aggregated performance metrics and trade logs of a backtest."""

    experiment_id: UUID
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    trades: List[Dict[str, Any]] = Field(default_factory=list)
    schema_version: int = Field(default=1)
