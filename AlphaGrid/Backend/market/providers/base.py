"""Provider abstraction layer — abstract interfaces and internal transport types.

No broker-specific logic lives in this file.

All downstream modules (ConnectorManager, OHLCV engine, etc.) import from here.
Only the concrete adapter files in this package import broker SDKs.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from enum import StrEnum


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class ProviderStatus(StrEnum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNAVAILABLE = "UNAVAILABLE"


class ValidationStatus(StrEnum):
    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"


# ---------------------------------------------------------------------------
# Internal transport dataclasses
#
# These are pipeline-internal only. They are NEVER exposed to routers or DTOs.
# The normalizer converts these into Shared domain types or plain dicts.
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ProviderHealth:
    """Health snapshot for a single provider."""

    provider_name: str
    status: ProviderStatus
    latency_ms: float
    message: str = ""


@dataclass(frozen=True, slots=True)
class InstrumentRecord:
    """Raw instrument record as returned by a provider (before normalization)."""

    symbol: str
    exchange: str          # Provider-native value, e.g. "NSE_EQ" or "NSE"
    segment: str           # e.g. "EQ", "FO", "INDEX"
    instrument_type: str   # "STOCK", "INDEX", "FUTURE", "OPTION"
    display_name: str
    lot_size: int
    tick_size: Decimal
    expiry_date: str | None = None       # ISO-8601 date string
    strike_price: Decimal | None = None
    option_type: str | None = None       # "CE" or "PE"
    isin: str | None = None
    trading_symbol: str | None = None    # Broker-specific symbol


@dataclass(frozen=True, slots=True)
class OHLCVRecord:
    """Raw OHLCV record as returned by a provider (before normalization)."""

    symbol: str
    exchange: str
    timeframe: str         # "1m", "5m", "15m", "1h", "1d"
    timestamp: datetime    # Must be UTC-aware after normalization
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int


@dataclass(frozen=True, slots=True)
class LiveQuoteRecord:
    """Raw live price snapshot as returned by a provider (before normalization)."""

    symbol: str
    exchange: str
    last_price: Decimal
    bid: Decimal
    ask: Decimal
    high: Decimal
    low: Decimal
    open: Decimal
    prev_close: Decimal
    volume: int
    timestamp: datetime    # UTC-aware
    change: Decimal = field(default_factory=lambda: Decimal("0"))
    change_pct: Decimal = field(default_factory=lambda: Decimal("0"))


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Result of validating a single OHLCV record."""

    status: ValidationStatus
    reason: str | None = None


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class ProviderUnavailable(Exception):
    """Raised when a provider is not configured, credentials missing, or unreachable.

    The ConnectorManager catches this and tries the next provider in priority order.
    """

    def __init__(self, provider_name: str, reason: str = "") -> None:
        super().__init__(f"Provider '{provider_name}' unavailable: {reason}")
        self.provider_name = provider_name
        self.reason = reason


class ConnectorError(Exception):
    """Raised when all providers in the ConnectorManager have failed."""


class ProviderRateLimitError(ProviderUnavailable):
    """Raised when a provider returns a rate-limit or quota-exceeded response."""


# ---------------------------------------------------------------------------
# Abstract base interface — every provider must implement this
# ---------------------------------------------------------------------------


class MarketDataProvider(ABC):
    """Abstract contract for all market data providers.

    Concrete implementations live in the same package:
        yahoo.py, angelone.py, upstox.py, zerodha.py, mock.py

    Nothing outside this package (providers/) should import those files directly.
    All external consumers go through ConnectorManager.
    """

    # ------------------------------------------------------------------
    # Identity & Health
    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Human-readable unique provider identifier."""

    @abstractmethod
    def health_check(self) -> ProviderHealth:
        """Return a health snapshot for this provider.

        Must never raise — return UNAVAILABLE status on failure.
        """

    # ------------------------------------------------------------------
    # Instruments
    # ------------------------------------------------------------------

    @abstractmethod
    def get_instruments(
        self,
        exchange: str | None = None,
        segment: str | None = None,
    ) -> list[InstrumentRecord]:
        """Return the instrument catalog, optionally filtered by exchange/segment."""

    # ------------------------------------------------------------------
    # Historical OHLCV
    # ------------------------------------------------------------------

    @abstractmethod
    def get_ohlcv(
        self,
        symbol: str,
        exchange: str,
        timeframe: str,
        from_dt: datetime,
        to_dt: datetime,
    ) -> list[OHLCVRecord]:
        """Return historical OHLCV candles for the given symbol and timeframe.

        Timestamps in returned records may be in provider-local timezone;
        the normalizer converts them to UTC.

        Raises:
            ProviderUnavailable: if the provider cannot fulfil the request.
        """

    # ------------------------------------------------------------------
    # Live Quotes
    # ------------------------------------------------------------------

    @abstractmethod
    def get_live_quote(self, symbol: str, exchange: str) -> LiveQuoteRecord:
        """Return the latest live price snapshot for a single symbol.

        Raises:
            ProviderUnavailable: if the provider cannot fulfil the request.
        """

    @abstractmethod
    def get_live_quotes(
        self, symbols: list[tuple[str, str]]
    ) -> list[LiveQuoteRecord]:
        """Return live price snapshots for a batch of (symbol, exchange) pairs.

        Raises:
            ProviderUnavailable: if the provider cannot fulfil the request.
        """

    # ------------------------------------------------------------------
    # Helpers available to all providers
    # ------------------------------------------------------------------

    @staticmethod
    def timeframe_to_delta(timeframe: str) -> timedelta:
        """Convert a timeframe string to a timedelta for iteration."""
        _map: dict[str, timedelta] = {
            "1m": timedelta(minutes=1),
            "5m": timedelta(minutes=5),
            "15m": timedelta(minutes=15),
            "30m": timedelta(minutes=30),
            "1h": timedelta(hours=1),
            "4h": timedelta(hours=4),
            "1d": timedelta(days=1),
            "1w": timedelta(weeks=1),
        }
        delta = _map.get(timeframe)
        if delta is None:
            raise ValueError(f"Unknown timeframe: '{timeframe}'")
        return delta
