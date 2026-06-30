"""Dashboard domain router — /api/v1/dashboard/"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from Backend.api.responses import success_response
from Backend.api.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
_service = DashboardService()


class SaveLayoutBody(BaseModel):
    """Request body for saving a dashboard widget layout."""

    widgets: list[dict[str, Any]] = Field(default_factory=list)
    version: int = Field(default=1, ge=1)


@router.get("", summary="Dashboard summary data")
def get_dashboard() -> JSONResponse:
    """Return the combined dashboard summary: market, portfolio, and system state."""
    data = _service.get_dashboard_summary()
    return success_response(data=data)


@router.get("/layout", summary="Dashboard layout")
def get_layout() -> JSONResponse:
    """Return the user's current saved dashboard widget layout."""
    data = _service.get_layout()
    return success_response(data=data)


@router.put("/layout", summary="Save dashboard layout")
def save_layout(body: SaveLayoutBody) -> JSONResponse:
    """Persist a new dashboard widget layout configuration."""
    data = _service.save_layout(layout=body.model_dump())
    return success_response(data=data, message="Layout saved.")
