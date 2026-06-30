"""Features service stub.

Interface contract for the feature domain. Real implementation belongs in
the Feature Engineering phase.
"""

from __future__ import annotations

from typing import Any


class FeaturesService:
    """Stub service for technical and market feature operations."""

    def get_latest_features(
        self, symbol: str, timeframe: str | None = None
    ) -> dict[str, Any]:
        """Return the most recently computed feature set for a symbol."""
        return {"symbol": symbol, "timeframe": timeframe, "features": {}}

    def get_feature_history(
        self,
        symbol: str,
        timeframe: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> list[dict[str, Any]]:
        """Return the historical feature record for a symbol."""
        return []

    def recalculate_features(self, symbol: str, timeframe: str | None = None) -> dict[str, Any]:
        """Trigger an async recalculation of features for a given symbol."""
        return {"status": "queued", "symbol": symbol, "timeframe": timeframe}
