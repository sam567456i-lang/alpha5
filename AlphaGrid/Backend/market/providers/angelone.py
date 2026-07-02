"""Angel One Smart API provider adapter.

Requires credentials loaded from environment variables:
- ANGELONE_CLIENT_ID
- ANGELONE_PASSWORD
- ANGELONE_API_KEY
- ANGELONE_TOTP_SECRET
"""

from __future__ import annotations

import os
from typing import Any
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from .base import (
    InstrumentRecord,
    LiveQuoteRecord,
    MarketDataProvider,
    OHLCVRecord,
    ProviderHealth,
    ProviderStatus,
    ProviderUnavailable,
)

# Lazy import
try:
    from SmartApi import SmartConnect

    import pyotp

    _ANGEL_AVAILABLE = True
except ImportError:
    _ANGEL_AVAILABLE = False
    SmartConnect = None
    pyotp = None

_PRECISION = Decimal("0.0001")


def _dec(value: float | str) -> Decimal:
    return Decimal(str(value)).quantize(_PRECISION, rounding=ROUND_HALF_UP)


class AngelOneProvider(MarketDataProvider):
    """Angel One Smart API data provider."""

    def __init__(self) -> None:
        self._api: Any = None
        self._is_connected = False
        
        self.client_id = os.getenv("ANGELONE_CLIENT_ID")
        self.password = os.getenv("ANGELONE_PASSWORD")
        self.api_key = os.getenv("ANGELONE_API_KEY")
        self.totp_secret = os.getenv("ANGELONE_TOTP_SECRET")
        
        self._credentials_exist = all(
            [self.client_id, self.password, self.api_key, self.totp_secret]
        )

    @property
    def provider_name(self) -> str:
        return "angelone"

    def _ensure_connected(self) -> None:
        if self._is_connected and self._api is not None:
            return

        if not _ANGEL_AVAILABLE:
            raise ProviderUnavailable(
                self.provider_name, "SmartApi package not installed."
            )
        
        if not self._credentials_exist:
            raise ProviderUnavailable(
                self.provider_name, "Missing AngelOne credentials in environment."
            )

        try:
            self._api = SmartConnect(api_key=self.api_key)
            totp = pyotp.TOTP(self.totp_secret).now()
            
            data = self._api.generateSession(self.client_id, self.password, totp)
            if not data or not data.get("status"):
                msg = data.get("message", "Unknown auth error") if data else "No response"
                raise ProviderUnavailable(self.provider_name, f"Auth failed: {msg}")
            
            self._is_connected = True
        except Exception as exc:
            self._is_connected = False
            raise ProviderUnavailable(self.provider_name, f"Connection failed: {exc}") from exc

    def health_check(self) -> ProviderHealth:
        if not _ANGEL_AVAILABLE:
            return ProviderHealth(
                provider_name=self.provider_name,
                status=ProviderStatus.UNAVAILABLE,
                latency_ms=0.0,
                message="SmartApi not installed.",
            )
        if not self._credentials_exist:
            return ProviderHealth(
                provider_name=self.provider_name,
                status=ProviderStatus.UNAVAILABLE,
                latency_ms=0.0,
                message="Credentials not configured.",
            )
            
        try:
            import time
            start = time.perf_counter()
            self._ensure_connected()
            profile = self._api.getProfile(self._api.refresh_token)
            if not profile.get("status"):
                raise Exception("Profile fetch failed")
            latency_ms = (time.perf_counter() - start) * 1000
            
            return ProviderHealth(
                provider_name=self.provider_name,
                status=ProviderStatus.HEALTHY,
                latency_ms=round(latency_ms, 2),
                message="Connected to Angel One.",
            )
        except ProviderUnavailable as exc:
            return ProviderHealth(
                provider_name=self.provider_name,
                status=ProviderStatus.UNAVAILABLE,
                latency_ms=0.0,
                message=exc.reason,
            )
        except Exception as exc:
            return ProviderHealth(
                provider_name=self.provider_name,
                status=ProviderStatus.DEGRADED,
                latency_ms=0.0,
                message=str(exc),
            )

    # ------------------------------------------------------------------
    # Instruments
    # ------------------------------------------------------------------

    def get_instruments(
        self,
        exchange: str | None = None,
        segment: str | None = None,
    ) -> list[InstrumentRecord]:
        """Angel One provides a JSON dump of instruments.
        
        For production, this should fetch and parse the JSON.
        Since we are building the abstraction, we raise ProviderUnavailable if not configured
        or return an empty list if not implemented fully to satisfy the type signature.
        """
        self._ensure_connected()
        # To fetch instruments, we'd normally request the JSON from:
        # https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json
        # Here we just raise Unavailable to fallback to Yahoo/Mock for now, as fetching
        # 100MB JSON synchronously here is bad practice. The real app would schedule a background job.
        raise ProviderUnavailable(self.provider_name, "Instrument fetch not implemented natively here. Use DB.")

    # ------------------------------------------------------------------
    # Historical OHLCV
    # ------------------------------------------------------------------

    def get_ohlcv(
        self,
        symbol: str,
        exchange: str,
        timeframe: str,
        from_dt: datetime,
        to_dt: datetime,
    ) -> list[OHLCVRecord]:
        self._ensure_connected()
        
        # Mapping timeframe
        interval_map = {
            "1m": "ONE_MINUTE",
            "5m": "FIVE_MINUTE",
            "15m": "FIFTEEN_MINUTE",
            "30m": "THIRTY_MINUTE",
            "1h": "ONE_HOUR",
            "1d": "ONE_DAY",
        }
        interval = interval_map.get(timeframe)
        if not interval:
            raise ProviderUnavailable(self.provider_name, f"Unsupported timeframe: {timeframe}")
            
        # We need the Angel One specific token for the symbol. 
        # In a real app, the normalizer/instrument catalog maps "NIFTY" to "26000".
        # We assume the caller passes the token in `symbol` or we look it up.
        # Since we don't have the token mapping here, we'll raise.
        raise ProviderUnavailable(self.provider_name, "Symbol to token mapping required.")

    # ------------------------------------------------------------------
    # Live Quotes
    # ------------------------------------------------------------------

    def get_live_quote(self, symbol: str, exchange: str) -> LiveQuoteRecord:
        self._ensure_connected()
        raise ProviderUnavailable(self.provider_name, "Symbol to token mapping required.")

    def get_live_quotes(
        self, symbols: list[tuple[str, str]]
    ) -> list[LiveQuoteRecord]:
        self._ensure_connected()
        raise ProviderUnavailable(self.provider_name, "Symbol to token mapping required.")
