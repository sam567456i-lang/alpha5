"""System domain router — /api/v1/system/"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from Backend.api.responses import success_response
from Backend.api.dependencies import get_system_service
from Backend.api.services.system_service import SystemService
from fastapi import Depends

router = APIRouter(prefix="/system", tags=["System"])


@router.get("/status", summary="System health status")
def get_system_status(service: SystemService = Depends(get_system_service)) -> JSONResponse:
    """Return the overall system health and the status of every component."""
    data = service.get_system_status()
    return success_response(data=data)


@router.post("/live/start", summary="Start live mode", status_code=201)
def start_live(service: SystemService = Depends(get_system_service)) -> JSONResponse:
    """Transition the system from Offline to Live mode."""
    data = service.start_live()
    return success_response(data=data, message="Live mode starting.", status_code=201)


@router.post("/live/stop", summary="Stop live mode")
def stop_live(service: SystemService = Depends(get_system_service)) -> JSONResponse:
    """Transition the system from Live to Offline mode."""
    data = service.stop_live()
    return success_response(data=data, message="Live mode stopping.")


@router.post("/live/pause", summary="Pause live mode")
def pause_live(service: SystemService = Depends(get_system_service)) -> JSONResponse:
    """Pause all live data collection without a full shutdown."""
    data = service.pause_live()
    return success_response(data=data, message="Live mode paused.")


@router.post("/live/resume", summary="Resume live mode")
def resume_live(service: SystemService = Depends(get_system_service)) -> JSONResponse:
    """Resume previously paused live data collection."""
    data = service.resume_live()
    return success_response(data=data, message="Live mode resumed.")
