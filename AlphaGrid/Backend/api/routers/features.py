"""Features domain router — /api/v1/features/"""

from __future__ import annotations

from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse

from Backend.api.responses import success_response, created_response
from Backend.api.services.features_service import FeaturesService
from Backend.api.dependencies import get_features_service

router = APIRouter(prefix="/features", tags=["Features"])


@router.get("", summary="Latest computed features")
def get_latest_features(
    symbol: str = Query(..., description="Instrument symbol."),
    timeframe: str | None = Query(default=None, description="Feature timeframe."),
    service: FeaturesService = Depends(get_features_service)
) -> JSONResponse:
    """Return the most recently computed feature set for the specified symbol."""
    data = service.get_latest_features(symbol=symbol, timeframe=timeframe)
    return success_response(data=data)


@router.get("/history", summary="Feature history")
def get_feature_history(
    symbol: str = Query(..., description="Instrument symbol."),
    timeframe: str | None = Query(default=None, description="Feature timeframe."),
    from_date: str | None = Query(default=None, description="Start date (ISO-8601)."),
    to_date: str | None = Query(default=None, description="End date (ISO-8601)."),
    service: FeaturesService = Depends(get_features_service)
) -> JSONResponse:
    """Return the historical feature time series for the specified symbol."""
    data = service.get_feature_history(
        symbol=symbol,
        timeframe=timeframe,
        from_date=from_date,
        to_date=to_date,
    )
    return success_response(data=data)


@router.post("/recalculate", summary="Trigger feature recalculation", status_code=201)
def recalculate_features(
    symbol: str = Query(..., description="Instrument symbol."),
    timeframe: str | None = Query(default=None, description="Feature timeframe."),
    service: FeaturesService = Depends(get_features_service)
) -> JSONResponse:
    """Trigger an async recalculation of features for a given symbol and timeframe."""
    data = service.recalculate_features(symbol=symbol, timeframe=timeframe)
    return created_response(data=data, message="Feature recalculation queued.")
