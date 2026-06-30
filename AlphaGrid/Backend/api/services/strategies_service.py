"""Strategies service stub.

Interface contract for the strategy domain. Real implementation belongs in
the Strategy Platform phase.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID


class StrategiesService:
    """Stub service for strategy domain operations."""

    def list_strategies(self) -> list[dict[str, Any]]:
        """Return all registered strategies."""
        return []

    def get_strategy(self, strategy_id: UUID) -> dict[str, Any] | None:
        """Return a single strategy by ID, or None if not found."""
        return None

    def validate_strategy(self, strategy_id: UUID, parameters: dict[str, Any]) -> dict[str, Any]:
        """Run a paper validation pass for a strategy with given parameters."""
        return {"status": "queued", "strategy_id": str(strategy_id)}

    def run_backtest(
        self,
        strategy_id: UUID,
        start_date: str,
        end_date: str,
        parameters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Trigger a historical backtest for a given strategy and date range."""
        return {
            "status": "queued",
            "strategy_id": str(strategy_id),
            "start_date": start_date,
            "end_date": end_date,
        }
