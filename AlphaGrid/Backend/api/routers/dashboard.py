"""Dashboard domain router — /api/v1/dashboard/"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from Backend.api.responses import success_response
from Backend.api.dependencies import get_dashboard_service
from Backend.api.services.dashboard_service import DashboardService
from fastapi import Depends

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


class SaveLayoutBody(BaseModel):
    """Request body for saving a dashboard widget layout."""

    widgets: list[dict[str, Any]] = Field(default_factory=list)
    version: int = Field(default=1, ge=1)


@router.get("", summary="Dashboard summary data")
def get_dashboard(service: DashboardService = Depends(get_dashboard_service)) -> JSONResponse:
    """Return the combined dashboard summary: market, portfolio, and system state."""
    data = service.get_dashboard_summary()
    return success_response(data=data)


@router.get("/layout", summary="Dashboard layout")
def get_layout(service: DashboardService = Depends(get_dashboard_service)) -> JSONResponse:
    """Return the user's current saved dashboard widget layout."""
    data = service.get_layout()
    return success_response(data=data)


@router.put("/layout", summary="Save dashboard layout")
def save_layout(body: SaveLayoutBody, service: DashboardService = Depends(get_dashboard_service)) -> JSONResponse:
    """Persist a new dashboard widget layout configuration."""
    data = service.save_layout(layout=body.model_dump())
    return success_response(data=data, message="Layout saved.")
