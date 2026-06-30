"""Research domain router — /api/v1/research/"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from Backend.api.dependencies import PaginationParams, get_pagination
from Backend.api.responses import created_response, paginated_response
from Backend.api.services.research_service import ResearchService

router = APIRouter(prefix="/research", tags=["Research"])
_service = ResearchService()


class BacktestBody(BaseModel):
    """Request body for triggering a research backtest."""

    strategy: str = Field(..., min_length=1, description="Strategy name.")
    start_date: str = Field(..., description="Start date (ISO-8601).")
    end_date: str = Field(..., description="End date (ISO-8601).")
    parameters: dict[str, Any] = Field(default_factory=dict)


class ReplayBody(BaseModel):
    """Request body for starting a replay session."""

    symbol: str = Field(..., min_length=1, description="Instrument symbol.")
    date: str = Field(..., description="Replay date (ISO-8601).")
    timeframe: str | None = Field(default=None, description="Candle timeframe.")


@router.get("", summary="Research experiments")
def list_experiments(
    pagination: PaginationParams = Depends(get_pagination),
) -> JSONResponse:
    """Return paginated research experiments and their results."""
    records, total = _service.list_experiments(
        page=pagination.page, page_size=pagination.page_size
    )
    return paginated_response(
        data=records,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.post("/backtest", summary="Run research backtest", status_code=201)
def run_backtest(body: BacktestBody) -> JSONResponse:
    """Trigger a historical backtest for research purposes."""
    data = _service.run_backtest(
        strategy=body.strategy,
        start_date=body.start_date,
        end_date=body.end_date,
        parameters=body.parameters,
    )
    return created_response(data=data, message="Research backtest queued.")


@router.post("/replay", summary="Start replay session", status_code=201)
def start_replay(body: ReplayBody) -> JSONResponse:
    """Start a market replay session for historical analysis."""
    data = _service.start_replay(
        symbol=body.symbol,
        date=body.date,
        timeframe=body.timeframe,
    )
    return created_response(data=data, message="Replay session started.")
