"""Connector Manager — maintains the provider registry, priority, and failover logic."""

from __future__ import annotations

import logging
import threading
from datetime import datetime

from .providers.base import (
    ConnectorError,
    InstrumentRecord,
    LiveQuoteRecord,
    MarketDataProvider,
    OHLCVRecord,
    ProviderHealth,
    ProviderUnavailable,
)

logger = logging.getLogger(__name__)


class ConnectorManager:
    """Manages multiple data providers with automatic failover.

    The application interacts with this manager, not the providers directly.
    Providers are tried in order of priority (index 0 = primary).
    """

    def __init__(self) -> None:
        self._providers: list[MarketDataProvider] = []
        self._lock = threading.Lock()

    def register(self, provider: MarketDataProvider) -> None:
        """Register a provider at the lowest priority (end of the list)."""
        with self._lock:
            if any(p.provider_name == provider.provider_name for p in self._providers):
                return
            self._providers.append(provider)

    def set_priority(self, provider_names: list[str]) -> None:
        """Reorder providers based on the given list of names.

        Providers not in the list are placed at the end.
        """
        ordered: list[MarketDataProvider] = []
        for name in provider_names:
            for p in self._providers:
                if p.provider_name == name:
                    ordered.append(p)
                    break

        # Append any providers not explicitly ordered
        with self._lock:
            for p in self._providers:
                if p not in ordered:
                    ordered.append(p)

            self._providers = ordered

    def health_check_all(self) -> dict[str, ProviderHealth]:
        """Return health status for every registered provider."""
        return {p.provider_name: p.health_check() for p in self._providers}

    # ------------------------------------------------------------------
    # Data Access with Failover
    # ------------------------------------------------------------------

    def get_instruments(
        self,
        exchange: str | None = None,
        segment: str | None = None,
    ) -> list[InstrumentRecord]:
        errors = []
        with self._lock:
            providers_snapshot = list(self._providers)
        for provider in providers_snapshot:
            try:
                return provider.get_instruments(exchange, segment)
            except ProviderUnavailable as exc:
                errors.append(f"{provider.provider_name}: {exc.reason}")
                logger.debug("Provider '%s' unavailable for instruments: %s", provider.provider_name, exc.reason)
            except Exception as exc:
                errors.append(f"{provider.provider_name}: {exc}")
                logger.warning("Provider '%s' failed for instruments: %s", provider.provider_name, exc)

        raise ConnectorError(f"All providers failed to fetch instruments. Errors: {errors}")

    def get_ohlcv(
        self,
        symbol: str,
        exchange: str,
        timeframe: str,
        from_dt: datetime,
        to_dt: datetime,
    ) -> list[OHLCVRecord]:
        errors = []
        with self._lock:
            providers_snapshot = list(self._providers)
        for provider in providers_snapshot:
            try:
                return provider.get_ohlcv(symbol, exchange, timeframe, from_dt, to_dt)
            except ProviderUnavailable as exc:
                errors.append(f"{provider.provider_name}: {exc.reason}")
                logger.debug("Provider '%s' unavailable for OHLCV: %s", provider.provider_name, exc.reason)
            except Exception as exc:
                errors.append(f"{provider.provider_name}: {exc}")
                logger.warning("Provider '%s' failed for OHLCV: %s", provider.provider_name, exc)

        raise ConnectorError(f"All providers failed to fetch OHLCV for {symbol}. Errors: {errors}")

    def get_live_quote(self, symbol: str, exchange: str) -> LiveQuoteRecord:
        errors = []
        with self._lock:
            providers_snapshot = list(self._providers)
        for provider in providers_snapshot:
            try:
                return provider.get_live_quote(symbol, exchange)
            except ProviderUnavailable as exc:
                errors.append(f"{provider.provider_name}: {exc.reason}")
            except Exception as exc:
                errors.append(f"{provider.provider_name}: {exc}")
                logger.warning("Provider '%s' failed for live quote: %s", provider.provider_name, exc)

        raise ConnectorError(f"All providers failed to fetch quote for {symbol}. Errors: {errors}")

    def get_live_quotes(
        self, symbols: list[tuple[str, str]]
    ) -> list[LiveQuoteRecord]:
        """Fetch quotes in batch. Tries providers in order until one succeeds."""
        errors = []
        with self._lock:
            providers_snapshot = list(self._providers)
        for provider in providers_snapshot:
            try:
                # If a provider supports batch but misses some symbols, it should
                # return a partial list. We accept the partial list rather than failing over.
                results = provider.get_live_quotes(symbols)
                if results:
                    return results
            except ProviderUnavailable as exc:
                errors.append(f"{provider.provider_name}: {exc.reason}")
            except Exception as exc:
                errors.append(f"{provider.provider_name}: {exc}")
                logger.warning("Provider '%s' failed for live quotes batch: %s", provider.provider_name, exc)

        raise ConnectorError(f"All providers failed to fetch batch quotes. Errors: {errors}")
