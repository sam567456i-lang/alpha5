"""Upstox API v2 provider adapter.

Requires credentials loaded from environment variables:
- UPSTOX_API_KEY
- UPSTOX_API_SECRET
- UPSTOX_ACCESS_TOKEN
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
    import upstox_client

    _UPSTOX_AVAILABLE = True
except ImportError:
    _UPSTOX_AVAILABLE = False
    upstox_client = None


class UpstoxProvider(MarketDataProvider):
    """Upstox API v2 data provider."""

    def __init__(self) -> None:
        self.api_key = os.getenv("UPSTOX_API_KEY")
        self.api_secret = os.getenv("UPSTOX_API_SECRET")
        self.access_token = os.getenv("UPSTOX_ACCESS_TOKEN")
        
        self._credentials_exist = all([self.api_key, self.api_secret, self.access_token])
        self._is_connected = False
        self._api = None

    @property
    def provider_name(self) -> str:
        return "upstox"

    def _ensure_connected(self) -> None:
        if self._is_connected and self._api is not None:
            return

        if not _UPSTOX_AVAILABLE:
            raise ProviderUnavailable(
                self.provider_name, "upstox-python package not installed."
            )
            
        if not self._credentials_exist:
            raise ProviderUnavailable(
                self.provider_name, "Missing Upstox credentials in environment."
            )

        try:
            configuration = upstox_client.Configuration()
            configuration.access_token = self.access_token
            self._api = upstox_client.ApiClient(configuration)
            self._is_connected = True
        except Exception as exc:
            raise ProviderUnavailable(self.provider_name, f"Connection failed: {exc}") from exc

    def health_check(self) -> ProviderHealth:
        if not _UPSTOX_AVAILABLE:
            return ProviderHealth(
                provider_name=self.provider_name,
                status=ProviderStatus.UNAVAILABLE,
                latency_ms=0.0,
                message="upstox-python not installed.",
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
            # Upstox doesn't have a simple ping, so we check user profile
            user_api = upstox_client.UserApi(self._api)
            user_api.get_profile(self.api_key)
            latency_ms = (time.perf_counter() - start) * 1000
            
            return ProviderHealth(
                provider_name=self.provider_name,
                status=ProviderStatus.HEALTHY,
                latency_ms=round(latency_ms, 2),
                message="Connected to Upstox.",
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
