"""Data Normalizer — converts provider records into Shared domain models."""

from __future__ import annotations

from datetime import timezone
from decimal import ROUND_HALF_UP, Decimal

from Shared.models.market import MarketSnapshot

from .providers.base import LiveQuoteRecord, OHLCVRecord

_PRECISION = Decimal("0.0001")


class DataNormalizer:
    """Normalizes raw provider records into standardized Shared domain models."""

    @staticmethod
    def _normalize_symbol(symbol: str) -> str:
        """Strip provider-specific suffixes and standardize case."""
        s = symbol.upper()
        if s.endswith(".NS"):
            s = s[:-3]
        if s.endswith(".BO"):
            s = s[:-3]
        return s

    @staticmethod
    def _normalize_exchange(exchange: str) -> str:
        """Standardize exchange codes."""
        e = exchange.upper()
        if e in ("NSE_EQ", "NSE_FO"):
            return "NSE"
        if e in ("BSE_EQ", "BSE_FO"):
            return "BSE"
        return e

    @staticmethod
    def _normalize_price(price: Decimal) -> Decimal:
        """Round prices to 4 decimal places."""
        return price.quantize(_PRECISION, rounding=ROUND_HALF_UP)

    @classmethod
    def normalize_ohlcv(cls, record: OHLCVRecord) -> MarketSnapshot:
        """Convert an OHLCVRecord to a Shared MarketSnapshot."""
        # Ensure timestamp is UTC
        ts = record.timestamp
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        else:
            ts = ts.astimezone(timezone.utc)

        return MarketSnapshot(
            symbol=cls._normalize_symbol(record.symbol),
            exchange=cls._normalize_exchange(record.exchange),
            instrument_type="STOCK",
            timestamp=ts,
            last_price=cls._normalize_price(record.close),
            open=cls._normalize_price(record.open),
            high=cls._normalize_price(record.high),
            low=cls._normalize_price(record.low),
            close=cls._normalize_price(record.close),
            volume=record.volume,
        )

    @classmethod
    def normalize_live_quote(cls, record: LiveQuoteRecord) -> MarketSnapshot:
        """Convert a LiveQuoteRecord to a Shared MarketSnapshot.
        
        A live quote is essentially a snapshot of the current timeframe (e.g. daily).
        """
        ts = record.timestamp
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        else:
            ts = ts.astimezone(timezone.utc)

        return MarketSnapshot(
            symbol=cls._normalize_symbol(record.symbol),
            exchange=cls._normalize_exchange(record.exchange),
            instrument_type="STOCK",
            timestamp=ts,
            last_price=cls._normalize_price(record.last_price),
            open=cls._normalize_price(record.open),
            high=cls._normalize_price(record.high),
            low=cls._normalize_price(record.low),
            close=cls._normalize_price(record.last_price),
            volume=record.volume,
        )
