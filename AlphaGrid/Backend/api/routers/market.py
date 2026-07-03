"""Market domain router — /api/v1/market/"""

from __future__ import annotations

from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse

from Backend.api.responses import success_response
from Backend.api.dependencies import get_market_service
from Backend.api.services.market_service import MarketService

router = APIRouter(prefix="/market", tags=["Market"])


@router.get("/status", summary="Market session status")
def get_market_status(service: MarketService = Depends(get_market_service)) -> JSONResponse:
    """Return the current market session state (open/closed, session name)."""
    result = service.get_market_status()
    return success_response(
        data={
            "is_open": result.is_open,
            "session": result.session,
            "exchange": result.exchange,
            "message": result.message,
        }
    )


@router.get("/instruments", summary="Instrument catalog")
def get_instruments(
    exchange: str | None = Query(default=None, description="Filter by exchange code."),
    segment: str | None = Query(default=None, description="Filter by segment (Equity, F&O, Index)."),
    service: MarketService = Depends(get_market_service)
) -> JSONResponse:
    """Return the list of all tradable instruments."""
    data = service.get_instruments(exchange=exchange, segment=segment)
    return success_response(data=data)


@router.get("/ohlcv", summary="Historical OHLCV candles")
def get_ohlcv(
    symbol: str = Query(..., description="Instrument symbol."),
    timeframe: str = Query(default="15m", description="Candle timeframe (1m, 5m, 15m, 1h, 1d)."),
    from_date: str | None = Query(default=None, description="Start date (ISO-8601)."),
    to_date: str | None = Query(default=None, description="End date (ISO-8601)."),
    service: MarketService = Depends(get_market_service)
) -> JSONResponse:
    """Return historical OHLCV candle data for the specified symbol and timeframe."""
    data = service.get_ohlcv(
        symbol=symbol,
        timeframe=timeframe,
        from_date=from_date,
        to_date=to_date,
    )
    return success_response(data=data)


@router.get("/live", summary="Live price quotes")
def get_live_quotes(
    symbols: str | None = Query(
        default=None,
        description="Comma-separated list of symbols. Omit for all instruments.",
    ),
    service: MarketService = Depends(get_market_service)
) -> JSONResponse:
    """Return the latest live quotes for one or more instruments."""
    symbol_list = [s.strip() for s in symbols.split(",")] if symbols else None
    data = service.get_live_quotes(symbols=symbol_list)
    return success_response(data=data)


@router.get("/breadth", summary="Market breadth metrics")
def get_market_breadth(service: MarketService = Depends(get_market_service)) -> JSONResponse:
    """Return the current market breadth: advances, declines, AD ratio, breadth score."""
    data = service.get_market_breadth()
    return success_response(data=data)


@router.get("/regime", summary="Detected market regime")
def get_market_regime(service: MarketService = Depends(get_market_service)) -> JSONResponse:
    """Return the currently detected market regime and confidence score."""
    data = service.get_market_regime()
    return success_response(data=data)


@router.get("/calendar", summary="Economic calendar")
def get_economic_calendar(
    from_date: str | None = Query(default=None, description="Start date (ISO-8601)."),
    to_date: str | None = Query(default=None, description="End date (ISO-8601)."),
    service: MarketService = Depends(get_market_service)
) -> JSONResponse:
    """Return upcoming macroeconomic events that may affect trading."""
    data = service.get_economic_calendar(from_date=from_date, to_date=to_date)
    return success_response(data=data)


@router.get("/news", summary="Market news")
def get_news(
    limit: int = Query(default=20, ge=1, le=100, description="Number of articles to return."),
    category: str | None = Query(default=None, description="Filter by news category."),
    service: MarketService = Depends(get_market_service)
) -> JSONResponse:
    """Return recent market news articles."""
    data = service.get_news(limit=limit, category=category)
    return success_response(data=data)
