"""Strategies domain router — /api/v1/strategies/"""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from Backend.api.exceptions import APINotFoundError
from Backend.api.responses import created_response, success_response
from Backend.api.services.strategies_service import StrategiesService

router = APIRouter(prefix="/strategies", tags=["Strategies"])
_service = StrategiesService()


class ValidateStrategyBody(BaseModel):
    """Request body for strategy paper validation."""

    parameters: dict[str, Any] = Field(default_factory=dict)


class BacktestBody(BaseModel):
    """Request body for triggering a strategy backtest."""

    start_date: str = Field(..., description="Backtest start date (ISO-8601).")
    end_date: str = Field(..., description="Backtest end date (ISO-8601).")
    parameters: dict[str, Any] = Field(default_factory=dict)


@router.get("", summary="All registered strategies")
def list_strategies() -> JSONResponse:
    """Return all registered trading strategies."""
    data = _service.list_strategies()
    return success_response(data=data)


@router.get("/{strategy_id}", summary="Single strategy")
def get_strategy(strategy_id: UUID) -> JSONResponse:
    """Return a single strategy by its UUID."""
    data = _service.get_strategy(strategy_id)
    if data is None:
        raise APINotFoundError(f"Strategy '{strategy_id}' not found.")
    return success_response(data=data)


@router.post("/{strategy_id}/validate", summary="Run paper validation", status_code=201)
def validate_strategy(strategy_id: UUID, body: ValidateStrategyBody) -> JSONResponse:
    """Trigger a paper validation run for the specified strategy."""
    data = _service.validate_strategy(strategy_id, body.parameters)
    return created_response(data=data, message="Strategy validation queued.")


@router.post("/{strategy_id}/backtest", summary="Run backtest", status_code=201)
def run_backtest(strategy_id: UUID, body: BacktestBody) -> JSONResponse:
    """Trigger a historical backtest for the specified strategy."""
    data = _service.run_backtest(
        strategy_id=strategy_id,
        start_date=body.start_date,
        end_date=body.end_date,
        parameters=body.parameters,
    )
    return created_response(data=data, message="Backtest queued.")
