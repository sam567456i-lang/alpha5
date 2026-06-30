"""Dashboard service stub.

Interface contract for the dashboard domain. Real implementation belongs in
the Dashboard phase.
"""

from __future__ import annotations

from typing import Any


class DashboardService:
    """Stub service for dashboard domain operations."""

    def get_dashboard_summary(self) -> dict[str, Any]:
        """Return a combined summary of market, portfolio, and recommendations for the dashboard."""
        return {
            "market_regime": "UNKNOWN",
            "market_health": "UNKNOWN",
            "opportunity_count": 0,
            "portfolio_health": "UNKNOWN",
            "open_positions": 0,
            "today_pnl": "0.00",
            "system_status": "ONLINE",
        }

    def get_layout(self) -> dict[str, Any]:
        """Return the user's saved dashboard widget layout configuration."""
        return {"widgets": [], "version": 1}

    def save_layout(self, layout: dict[str, Any]) -> dict[str, Any]:
        """Persist a new dashboard widget layout configuration."""
        return {"status": "saved", "version": layout.get("version", 1)}
