"""Reports service stub.

Interface contract for the reports domain. Real implementation belongs in
the Analytics & Reports phase.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID


class ReportsService:
    """Stub service for reports domain operations."""

    def list_reports(
        self, page: int = 1, page_size: int = 50
    ) -> tuple[list[dict[str, Any]], int]:
        """Return paginated list of generated reports.

        Returns:
            A tuple of (records, total_count).
        """
        return [], 0

    def generate_report(
        self,
        report_type: str,
        parameters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Trigger report generation for a given type and parameters."""
        return {
            "status": "queued",
            "report_type": report_type,
            "parameters": parameters or {},
        }

    def get_report(self, report_id: UUID) -> dict[str, Any] | None:
        """Return a single report record with download URL, or None if not found."""
        return None
