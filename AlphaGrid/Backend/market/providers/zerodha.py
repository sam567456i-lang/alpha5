"""Zerodha Kite Connect provider adapter.

Requires credentials loaded from environment variables:
- KITE_API_KEY
- KITE_ACCESS_TOKEN
"""

from __future__ import annotations

import os
from datetime import datetime

from .base import (
    InstrumentRecord,
    LiveQuoteRecord,
    MarketDataProvider,
    OHLCVRecord,
    ProviderHealth,
    ProviderStatus,
    ProviderUnavailable,
)

try:
    import kiteconnect

    _KITE_AVAILABLE = True
except ImportError:
    _KITE_AVAILABLE = False
    kiteconnect = None


class ZerodhaProvider(MarketDataProvider):
    """Zerodha Kite Connect data provider."""

    def __init__(self) -> None:
        self.api_key = os.getenv("KITE_API_KEY")
        self.access_token = os.getenv("KITE_ACCESS_TOKEN")
        
        self._credentials_exist = all([self.api_key, self.access_token])
        self._is_connected = False
        self._api = None

    @property
    def provider_name(self) -> str:
        return "zerodha"

    def _ensure_connected(self) -> None:
        if self._is_connected and self._api is not None:
            return

        if not _KITE_AVAILABLE:
            raise ProviderUnavailable(
                self.provider_name, "kiteconnect package not installed."
            )
            
        if not self._credentials_exist:
            raise ProviderUnavailable(
                self.provider_name, "Missing Kite credentials in environment."
            )

        try:
            self._api = kiteconnect.KiteConnect(api_key=self.api_key)
            self._api.set_access_token(self.access_token)  # type: ignore
            self._is_connected = True
        except Exception as exc:
            raise ProviderUnavailable(self.provider_name, f"Connection failed: {exc}") from exc

    def health_check(self) -> ProviderHealth:
        if not _KITE_AVAILABLE:
            return ProviderHealth(
                provider_name=self.provider_name,
                status=ProviderStatus.UNAVAILABLE,
                latency_ms=0.0,
                message="kiteconnect not installed.",
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
            # Fetch profile to verify token
            self._api.profile()  # type: ignore
            latency_ms = (time.perf_counter() - start) * 1000
            
            return ProviderHealth(
                provider_name=self.provider_name,
                status=ProviderStatus.HEALTHY,
                latency_ms=round(latency_ms, 2),
                message="Connected to Zerodha Kite.",
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

    def get_instruments(
        self,
        exchange: str | None = None,
        segment: str | None = None,
    ) -> list[InstrumentRecord]:
        self._ensure_connected()
        raise ProviderUnavailable(self.provider_name, "Instrument fetch not implemented natively here. Use DB.")

    def get_ohlcv(
        self,
        symbol: str,
        exchange: str,
        timeframe: str,
        from_dt: datetime,
        to_dt: datetime,
    ) -> list[OHLCVRecord]:
        self._ensure_connected()
        raise ProviderUnavailable(self.provider_name, "Symbol to token mapping required.")

    def get_live_quote(self, symbol: str, exchange: str) -> LiveQuoteRecord:
        self._ensure_connected()
        raise ProviderUnavailable(self.provider_name, "Symbol to token mapping required.")

    def get_live_quotes(
        self, symbols: list[tuple[str, str]]
    ) -> list[LiveQuoteRecord]:
        self._ensure_connected()
        raise ProviderUnavailable(self.provider_name, "Symbol to token mapping required.")
