"""Response and WebSocket DTO models."""

from datetime import datetime
from typing import Any
from pydantic import Field
from Shared.models import (
    AIModel,
    Evidence,
    MarketSnapshot,
    Notification,
    Opportunity,
    Portfolio,
    Position,
    Recommendation,
    ResearchProject,
    Trade,
)
from Shared.models.common import AlphaGridBaseModel


class StandardResponse(AlphaGridBaseModel):
    """Unified API response payload wrapper."""

    success: bool
    message: str
    data: Any | None = Field(default=None)


class ErrorInfo(AlphaGridBaseModel):
    """Detailed error info properties."""

    code: str
    message: str
    details: list[Any] | None = Field(default=None)


class ErrorResponse(AlphaGridBaseModel):
    """Unified API error response payload wrapper."""

    success: bool = Field(default=False)
    error: ErrorInfo


class PortfolioResponse(AlphaGridBaseModel):
    """API response payload returning a portfolio."""

    portfolio: Portfolio


class TradeResponse(AlphaGridBaseModel):
    """API response payload returning a trade."""

    trade: Trade


class RecommendationResponse(AlphaGridBaseModel):
    """API response payload returning a recommendation."""

    recommendation: Recommendation


class ResearchProjectResponse(AlphaGridBaseModel):
    """API response payload returning a research project."""

    project: ResearchProject


class MarketUpdate(AlphaGridBaseModel):
    """WebSocket notification update containing a market snapshot."""

    type: str
    timestamp: datetime
    payload: MarketSnapshot


class RecommendationUpdate(AlphaGridBaseModel):
    """WebSocket notification update containing a recommendation."""

    type: str
    timestamp: datetime
    payload: Recommendation


class PortfolioUpdate(AlphaGridBaseModel):
    """WebSocket notification update containing a portfolio state."""

    type: str
    timestamp: datetime
    payload: Portfolio


class NotificationUpdate(AlphaGridBaseModel):
    """WebSocket notification update containing a system alert."""

    type: str
    timestamp: datetime
    payload: Notification
