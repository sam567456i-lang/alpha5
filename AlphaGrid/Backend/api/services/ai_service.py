"""AI service stub.

Interface contract for the AI domain. Real implementation belongs in
the AI Platform phase.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID


class AIService:
    """Stub service for AI domain operations."""

    def get_predictions(
        self, symbol: str | None = None, limit: int = 20
    ) -> list[dict[str, Any]]:
        """Return recent AI model predictions, optionally filtered by symbol."""
        return []

    def get_explanation(self, recommendation_id: UUID) -> dict[str, Any] | None:
        """Return AI-generated explanation for a specific recommendation."""
        return {
            "recommendation_id": str(recommendation_id),
            "explanation": "AI explanation not yet available. Service not implemented.",
            "feature_importance": [],
            "confidence_breakdown": {},
        }

    def list_models(self) -> list[dict[str, Any]]:
        """Return all registered AI models and their current status."""
        return []
