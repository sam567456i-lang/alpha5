"""Research service stub.

Interface contract for the research domain. Real implementation belongs in
the Research Platform phase.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID


class ResearchService:
    """Stub service for research domain operations."""

    def list_experiments(self, page: int = 1, page_size: int = 50) -> tuple[list[dict[str, Any]], int]:
        """Return paginated research experiments.

        Returns:
            A tuple of (records, total_count).
        """
        return [], 0

    def run_backtest(
        self,
        strategy: str,
        start_date: str,
        end_date: str,
        parameters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Trigger a backtest run for a given strategy and date range."""
        return {
            "status": "queued",
            "strategy": strategy,
            "start_date": start_date,
            "end_date": end_date,
        }

    def start_replay(
        self,
        symbol: str,
        date: str,
        timeframe: str | None = None,
    ) -> dict[str, Any]:
        """Start a market replay session for a given symbol and date."""
        return {
            "status": "started",
            "symbol": symbol,
            "date": date,
            "timeframe": timeframe,
        }
