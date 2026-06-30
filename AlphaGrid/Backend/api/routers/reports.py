"""Reports domain router — /api/v1/reports/"""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from Backend.api.dependencies import PaginationParams, get_pagination
from Backend.api.exceptions import APINotFoundError
from Backend.api.responses import created_response, paginated_response, success_response
from Backend.api.services.reports_service import ReportsService

router = APIRouter(prefix="/reports", tags=["Reports"])
_service = ReportsService()


class GenerateReportBody(BaseModel):
    """Request body for generating a new report."""

    report_type: str = Field(..., min_length=1, description="Type of report to generate.")
    parameters: dict[str, Any] = Field(default_factory=dict)


@router.get("", summary="All reports")
def list_reports(
    pagination: PaginationParams = Depends(get_pagination),
) -> JSONResponse:
    """Return a paginated list of generated reports."""
    records, total = _service.list_reports(
        page=pagination.page, page_size=pagination.page_size
    )
    return paginated_response(
        data=records,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.post("/generate", summary="Generate report", status_code=201)
def generate_report(body: GenerateReportBody) -> JSONResponse:
    """Trigger generation of a new report."""
    data = _service.generate_report(
        report_type=body.report_type,
        parameters=body.parameters,
    )
    return created_response(data=data, message="Report generation queued.")


@router.get("/{report_id}", summary="Download report")
def get_report(report_id: UUID) -> JSONResponse:
    """Return a single report record including download URL."""
    data = _service.get_report(report_id=report_id)
    if data is None:
        raise APINotFoundError(f"Report '{report_id}' not found.")
    return success_response(data=data)
