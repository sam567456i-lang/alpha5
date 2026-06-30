"""System domain router — /api/v1/system/"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from Backend.api.responses import success_response
from Backend.api.services.system_service import SystemService

router = APIRouter(prefix="/system", tags=["System"])
_service = SystemService()


@router.get("/status", summary="System health status")
def get_system_status() -> JSONResponse:
    """Return the overall system health and the status of every component."""
    data = _service.get_system_status()
    return success_response(data=data)


@router.post("/live/start", summary="Start live mode", status_code=201)
def start_live() -> JSONResponse:
    """Transition the system from Offline to Live mode."""
    data = _service.start_live()
    return success_response(data=data, message="Live mode starting.", status_code=201)


@router.post("/live/stop", summary="Stop live mode")
def stop_live() -> JSONResponse:
    """Transition the system from Live to Offline mode."""
    data = _service.stop_live()
    return success_response(data=data, message="Live mode stopping.")


@router.post("/live/pause", summary="Pause live mode")
def pause_live() -> JSONResponse:
    """Pause all live data collection without a full shutdown."""
    data = _service.pause_live()
    return success_response(data=data, message="Live mode paused.")


@router.post("/live/resume", summary="Resume live mode")
def resume_live() -> JSONResponse:
    """Resume previously paused live data collection."""
    data = _service.resume_live()
    return success_response(data=data, message="Live mode resumed.")
