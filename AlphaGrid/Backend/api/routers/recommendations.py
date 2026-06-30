"""Recommendations domain router — /api/v1/recommendations/"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from Backend.api.dependencies import PaginationParams, get_pagination
from Backend.api.exceptions import APINotFoundError
from Backend.api.responses import paginated_response, success_response
from Backend.api.services.recommendations_service import RecommendationsService
from fastapi import Depends

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])
_service = RecommendationsService()


@router.get("/live", summary="Current live recommendations")
def get_live_recommendations() -> JSONResponse:
    """Return all currently active recommendations."""
    data = _service.get_live_recommendations()
    return success_response(data=data)


@router.get("/history", summary="Historical recommendations")
def get_recommendation_history(
    symbol: str | None = Query(default=None, description="Filter by instrument symbol."),
    strategy: str | None = Query(default=None, description="Filter by strategy name."),
    pagination: PaginationParams = Depends(get_pagination),
) -> JSONResponse:
    """Return paginated historical recommendations, optionally filtered."""
    records, total = _service.get_recommendation_history(
        symbol=symbol,
        strategy=strategy,
        page=pagination.page,
        page_size=pagination.page_size,
    )
    return paginated_response(
        data=records,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{recommendation_id}", summary="Single recommendation details")
def get_recommendation(recommendation_id: UUID) -> JSONResponse:
    """Return the full detail of a single recommendation by its UUID."""
    data = _service.get_recommendation(recommendation_id)
    if data is None:
        raise APINotFoundError(f"Recommendation '{recommendation_id}' not found.")
    return success_response(data=data)
