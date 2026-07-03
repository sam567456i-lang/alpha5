"""AI domain router — /api/v1/ai/"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from Backend.api.responses import success_response
from Backend.api.dependencies import get_ai_service
from Backend.api.services.ai_service import AIService
from fastapi import Depends

router = APIRouter(prefix="/ai", tags=["AI"])


@router.get("/predictions", summary="Recent AI predictions")
def get_predictions(
    symbol: str | None = Query(default=None, description="Filter predictions by symbol."),
    limit: int = Query(default=20, ge=1, le=200, description="Max number of predictions."),
    service: AIService = Depends(get_ai_service)
) -> JSONResponse:
    """Return recent AI model predictions, optionally filtered by instrument."""
    data = service.get_predictions(symbol=symbol, limit=limit)
    return success_response(data=data)


@router.get("/explanation", summary="AI explanation for a recommendation")
def get_explanation(
    recommendation_id: UUID = Query(..., description="UUID of the recommendation to explain."),
    service: AIService = Depends(get_ai_service)
) -> JSONResponse:
    """Return the AI-generated explanation for a specific recommendation."""
    data = service.get_explanation(recommendation_id=recommendation_id)
    return success_response(data=data)


@router.get("/models", summary="Registered AI models")
def list_models(service: AIService = Depends(get_ai_service)) -> JSONResponse:
    """Return all registered AI models and their current deployment status."""
    data = service.list_models()
    return success_response(data=data)
