"""Recommendations service stub.

Interface contract for the recommendation domain. Real implementation belongs
in the Recommendation Engine phase.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID


class RecommendationsService:
    """Stub service for recommendation domain operations."""

    def get_live_recommendations(self) -> list[dict[str, Any]]:
        """Return all currently active (live) recommendations."""
        return []

    def get_recommendation_history(
        self,
        symbol: str | None = None,
        strategy: str | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> tuple[list[dict[str, Any]], int]:
        """Return paginated historical recommendations.

        Returns:
            A tuple of (records, total_count).
        """
        return [], 0

    def get_recommendation(self, recommendation_id: UUID) -> dict[str, Any] | None:
        """Return a single recommendation by ID, or None if not found."""
        return None
