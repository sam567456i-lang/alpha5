"""Mock provider — deterministic in-memory market data for testing.

Never makes network calls. All data is synthetically generated from a seeded
random number generator, so the same inputs always produce the same outputs.

Usage:
    from Backend.market.providers.mock import MockProvider
    provider = MockProvider()
"""

from __future__ import annotations

import random
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

from .base import (
    InstrumentRecord,
    LiveQuoteRecord,
    MarketDataProvider,
    OHLCVRecord,
    ProviderHealth,
    ProviderStatus,
)

# ---------------------------------------------------------------------------
# Seed instrument catalog
# ---------------------------------------------------------------------------

_INSTRUMENTS: list[InstrumentRecord] = [
    InstrumentRecord(
        symbol="NIFTY",
        exchange="NSE",
        segment="INDEX",
        instrument_type="INDEX",
        display_name="NIFTY 50",
        lot_size=50,
        tick_size=Decimal("0.05"),
    ),
    InstrumentRecord(
        symbol="BANKNIFTY",
        exchange="NSE",
        segment="INDEX",
        instrument_type="INDEX",
        display_name="BANK NIFTY",
        lot_size=15,
        tick_size=Decimal("0.05"),
    ),
    InstrumentRecord(
        symbol="FINNIFTY",
        exchange="NSE",
        segment="INDEX",
        instrument_type="INDEX",
        display_name="NIFTY FIN SERVICE",
        lot_size=40,
        tick_size=Decimal("0.05"),
    ),
    InstrumentRecord(
        symbol="RELIANCE",
        exchange="NSE",
        segment="EQ",
        instrument_type="STOCK",
        display_name="Reliance Industries Ltd",
        lot_size=1,
        tick_size=Decimal("0.05"),
        isin="INE002A01018",
    ),
    InstrumentRecord(
        symbol="HDFCBANK",
        exchange="NSE",
        segment="EQ",
        instrument_type="STOCK",
        display_name="HDFC Bank Ltd",
        lot_size=1,
        tick_size=Decimal("0.05"),
        isin="INE040A01034",
    ),
    InstrumentRecord(
        symbol="TCS",
        exchange="NSE",
        segment="EQ",
        instrument_type="STOCK",
        display_name="Tata Consultancy Services Ltd",
        lot_size=1,
        tick_size=Decimal("0.05"),
        isin="INE467B01029",
    ),
]

# Base prices used as random-walk seeds
_BASE_PRICES: dict[str, float] = {
    "NIFTY": 24000.0,
    "BANKNIFTY": 52000.0,
    "FINNIFTY": 23000.0,
    "RELIANCE": 2900.0,
    "HDFCBANK": 1750.0,
    "TCS": 3800.0,
}


def _precision(value: float, places: int = 4) -> Decimal:
    """Round a float to a fixed-precision Decimal."""
    return Decimal(str(value)).quantize(
        Decimal(10) ** -places, rounding=ROUND_HALF_UP
    )


class MockProvider(MarketDataProvider):
    """Deterministic in-memory provider for testing.

    Calling ``get_ohlcv("NIFTY", "NSE", "15m", from_dt, to_dt)`` always returns
    the same records for the same inputs — the RNG is seeded by symbol+timeframe.
    """

    @property
    def provider_name(self) -> str:
        return "mock"

    def health_check(self) -> ProviderHealth:
        return ProviderHealth(
            provider_name=self.provider_name,
            status=ProviderStatus.HEALTHY,
            latency_ms=0.1,
            message="Mock provider always healthy.",
        )

    # ------------------------------------------------------------------
    # Instruments
    # ------------------------------------------------------------------

    def get_instruments(
        self,
        exchange: str | None = None,
        segment: str | None = None,
    ) -> list[InstrumentRecord]:
        result = list(_INSTRUMENTS)
        if exchange:
            result = [i for i in result if i.exchange == exchange.upper()]
        if segment:
            result = [i for i in result if i.segment == segment.upper()]
        return result

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
        rng = random.Random(hash(f"{symbol.upper()}:{timeframe}"))
        delta = self.timeframe_to_delta(timeframe)
        base = _BASE_PRICES.get(symbol.upper(), 1000.0)

        records: list[OHLCVRecord] = []
        current = from_dt.replace(tzinfo=timezone.utc) if from_dt.tzinfo is None else from_dt
        to_dt = to_dt.replace(tzinfo=timezone.utc) if to_dt.tzinfo is None else to_dt

        price = base
        while current < to_dt and len(records) < 500:
            change = rng.uniform(-price * 0.005, price * 0.005)
            open_p = price
            close_p = max(0.01, price + change)
            high_p = max(open_p, close_p) + abs(rng.uniform(0, price * 0.002))
            low_p = min(open_p, close_p) - abs(rng.uniform(0, price * 0.002))
            volume = rng.randint(10_000, 2_000_000)

            records.append(
                OHLCVRecord(
                    symbol=symbol.upper(),
                    exchange=exchange.upper(),
                    timeframe=timeframe,
                    timestamp=current,
                    open=_precision(open_p),
                    high=_precision(high_p),
                    low=_precision(low_p),
                    close=_precision(close_p),
                    volume=volume,
                )
            )
            price = close_p
            current = current + delta

        return records

    # ------------------------------------------------------------------
    # Live Quotes
    # ------------------------------------------------------------------

    def get_live_quote(self, symbol: str, exchange: str) -> LiveQuoteRecord:
        rng = random.Random(hash(f"quote:{symbol.upper()}"))
        base = _BASE_PRICES.get(symbol.upper(), 1000.0)
        last = _precision(base + rng.uniform(-base * 0.01, base * 0.01))
        prev_close = _precision(base)
        change = last - prev_close
        change_pct = (change / prev_close * 100).quantize(
            Decimal("0.0001"), rounding=ROUND_HALF_UP
        )

        return LiveQuoteRecord(
            symbol=symbol.upper(),
            exchange=exchange.upper(),
            last_price=last,
            bid=last - _precision(0.05),
            ask=last + _precision(0.05),
            high=last + _precision(rng.uniform(10, 80)),
            low=last - _precision(rng.uniform(10, 80)),
            open=prev_close + _precision(rng.uniform(-20, 20)),
            prev_close=prev_close,
            volume=rng.randint(100_000, 10_000_000),
            timestamp=datetime.now(tz=timezone.utc),
            change=change,
            change_pct=change_pct,
        )

    def get_live_quotes(
        self, symbols: list[tuple[str, str]]
    ) -> list[LiveQuoteRecord]:
        return [self.get_live_quote(sym, exch) for sym, exch in symbols]
