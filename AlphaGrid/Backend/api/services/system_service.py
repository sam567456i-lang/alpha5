"""System service stub.

Interface contract for the system domain. Real implementation coordinates with
Foundation's LifecycleManager, HealthChecker, and the event bus.
"""

from __future__ import annotations

from typing import Any


class SystemService:
    """Stub service for system control and health operations."""

    def get_system_status(self) -> dict[str, Any]:
        """Return the overall system health and component statuses."""
        return {
            "status": "ONLINE",
            "version": "5.0.0",
            "components": {
                "database": "UNKNOWN",
                "redis": "UNKNOWN",
                "scheduler": "OFFLINE",
                "ai": "OFFLINE",
                "market_connection": "OFFLINE",
            },
            "live_mode": "OFFLINE",
        }

    def start_live(self) -> dict[str, Any]:
        """Transition the system from Offline to Live mode."""
        return {"status": "STARTING", "message": "Live mode starting."}

    def stop_live(self) -> dict[str, Any]:
        """Transition the system from Live to Offline mode."""
        return {"status": "STOPPING", "message": "Live mode stopping."}

    def pause_live(self) -> dict[str, Any]:
        """Pause all live data collection without full shutdown."""
        return {"status": "PAUSED", "message": "Live mode paused."}

    def resume_live(self) -> dict[str, Any]:
        """Resume paused live data collection."""
        return {"status": "LIVE", "message": "Live mode resumed."}
