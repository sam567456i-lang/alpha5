"""Portfolio domain router — /api/v1/portfolio/"""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from Backend.api.exceptions import APINotFoundError
from Backend.api.responses import created_response, no_content_response, success_response
from Backend.api.services.portfolio_service import PortfolioService
from Shared.enums import TradeDirection

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])
_service = PortfolioService()


class CreateTradeBody(BaseModel):
    """Request body for recording a new manual trade."""

    symbol: str = Field(..., min_length=1, description="Instrument symbol.")
    trade_type: TradeDirection = Field(..., description="BUY or SELL.")
    quantity: int = Field(..., gt=0, description="Number of lots/shares.")
    entry_price: float = Field(..., gt=0, description="Entry price per unit.")
    notes: str | None = Field(default=None, description="Optional trade notes.")


class UpdateTradeBody(BaseModel):
    """Request body for updating an existing manual trade."""

    exit_price: float | None = Field(default=None, gt=0, description="Exit price per unit.")
    notes: str | None = Field(default=None, description="Updated trade notes.")
    status: str | None = Field(default=None, description="Updated trade status.")


@router.get("", summary="Portfolio summary")
def get_portfolio() -> JSONResponse:
    """Return the current portfolio state including positions, trades, and PnL."""
    data = _service.get_portfolio()
    return success_response(data=data)


@router.post("/trades", summary="Add manual trade", status_code=201)
def add_trade(body: CreateTradeBody) -> JSONResponse:
    """Record a new manually entered trade."""
    from decimal import Decimal
    data = _service.add_trade(
        symbol=body.symbol,
        trade_type=body.trade_type,
        quantity=body.quantity,
        entry_price=Decimal(str(body.entry_price)),
        notes=body.notes,
    )
    return created_response(data=data, message="Trade recorded successfully.")


@router.put("/trades/{trade_id}", summary="Update trade")
def update_trade(trade_id: UUID, body: UpdateTradeBody) -> JSONResponse:
    """Update an existing manual trade record."""
    updates: dict[str, Any] = body.model_dump(exclude_none=True)
    data = _service.update_trade(trade_id=trade_id, updates=updates)
    if data is None:
        raise APINotFoundError(f"Trade '{trade_id}' not found.")
    return success_response(data=data, message="Trade updated successfully.")


@router.delete("/trades/{trade_id}", summary="Archive trade", status_code=204)
def archive_trade(trade_id: UUID) -> JSONResponse:
    """Soft-archive a manual trade. The record is retained for historical analysis."""
    found = _service.archive_trade(trade_id=trade_id)
    if not found:
        raise APINotFoundError(f"Trade '{trade_id}' not found.")
    return no_content_response()
