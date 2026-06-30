"""Options domain router — /api/v1/options/"""

from __future__ import annotations

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from Backend.api.responses import success_response
from Backend.api.services.options_service import OptionsService

router = APIRouter(prefix="/options", tags=["Options"])
_service = OptionsService()


@router.get("/chain", summary="Option chain")
def get_option_chain(
    symbol: str = Query(..., description="Underlying instrument symbol."),
    expiry: str | None = Query(default=None, description="Expiry date (ISO-8601). Defaults to near expiry."),
) -> JSONResponse:
    """Return the full option chain for the specified underlying and expiry."""
    data = _service.get_option_chain(symbol=symbol, expiry=expiry)
    return success_response(data=data)


@router.get("/greeks", summary="Option Greeks")
def get_greeks(
    symbol: str = Query(..., description="Underlying instrument symbol."),
    expiry: str | None = Query(default=None, description="Expiry date (ISO-8601)."),
) -> JSONResponse:
    """Return option Greeks (Delta, Gamma, Theta, Vega) for a given underlying."""
    data = _service.get_greeks(symbol=symbol, expiry=expiry)
    return success_response(data=data)


@router.get("/iv", summary="Implied Volatility")
def get_implied_volatility(
    symbol: str = Query(..., description="Underlying instrument symbol."),
    expiry: str | None = Query(default=None, description="Expiry date (ISO-8601)."),
) -> JSONResponse:
    """Return the implied volatility surface for a given underlying."""
    data = _service.get_implied_volatility(symbol=symbol, expiry=expiry)
    return success_response(data=data)


@router.get("/pcr", summary="Put-Call Ratio")
def get_pcr(
    symbol: str = Query(..., description="Underlying instrument symbol."),
) -> JSONResponse:
    """Return the Put-Call Ratio for the specified underlying."""
    data = _service.get_pcr(symbol=symbol)
    return success_response(data=data)


@router.get("/max-pain", summary="Max Pain")
def get_max_pain(
    symbol: str = Query(..., description="Underlying instrument symbol."),
    expiry: str | None = Query(default=None, description="Expiry date (ISO-8601)."),
) -> JSONResponse:
    """Return the Max Pain strike price for the specified expiry."""
    data = _service.get_max_pain(symbol=symbol, expiry=expiry)
    return success_response(data=data)
