"""Yahoo Finance provider — default free development provider.

Uses the ``yfinance`` library (unofficial Yahoo Finance wrapper).
No API key required. Suitable for historical OHLCV and basic live quotes.

Limitations (document so contributors know):
- Unofficial interface — Yahoo may change the underlying API without notice.
- Live quotes are delayed by ~15 minutes for most instruments.
- Option chain support is limited and not suitable for Indian F&O.
- NSE symbols require the ``.NS`` suffix; BSE requires ``.BO``.
- Not recommended as a production live-data source.

Credentials: None required.
Environment variables: None required.
"""

from __future__ import annotations

import time
from datetime import datetime, timezone
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

# Lazy import so that the package remains importable even when yfinance is absent.
try:
    import yfinance as _yf


    _YFINANCE_AVAILABLE = True
except ImportError:
    _yf = None

    _YFINANCE_AVAILABLE = False

# ---------------------------------------------------------------------------
# Exchange suffix mapping  (AlphaGrid exchange → Yahoo Finance suffix)
# ---------------------------------------------------------------------------

_EXCHANGE_SUFFIX: dict[str, str] = {
    "NSE": ".NS",
    "BSE": ".BO",
}

# Timeframe mapping (AlphaGrid → yfinance interval string)
_TIMEFRAME_MAP: dict[str, str] = {
    "1m": "1m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "1h",
    "4h": "1h",   # yfinance has no 4h; fall back to 1h
    "1d": "1d",
    "1w": "1wk",
}

_PRECISION = Decimal("0.0001")


def _dec(value: float) -> Decimal:
    return Decimal(str(value)).quantize(_PRECISION, rounding=ROUND_HALF_UP)


class YahooFinanceProvider(MarketDataProvider):
    """Yahoo Finance market data adapter (free, no credentials required).

    Treat as the development/default provider. For production live data use
    Angel One, Upstox, or Zerodha.
    """

    @property
    def provider_name(self) -> str:
        return "yahoo_finance"

    def _require_yfinance(self) -> None:
        if not _YFINANCE_AVAILABLE:
            raise ProviderUnavailable(
                self.provider_name,
                "yfinance is not installed. Run: pip install yfinance",
            )

    def _yahoo_symbol(self, symbol: str, exchange: str) -> str:
        """Convert internal symbol + exchange to a Yahoo Finance ticker."""
        sym = symbol.upper()
        if sym == "NIFTY":
            return "^NSEI"
        if sym == "BANKNIFTY":
            return "^NSEBANK"
        if sym == "FINNIFTY":
            return "^CNXFIN"
            
        suffix = _EXCHANGE_SUFFIX.get(exchange.upper(), ".NS")
        return f"{sym}{suffix}"

    def health_check(self) -> ProviderHealth:
        if not _YFINANCE_AVAILABLE:
            return ProviderHealth(
                provider_name=self.provider_name,
                status=ProviderStatus.UNAVAILABLE,
                latency_ms=0.0,
                message="yfinance not installed.",
            )
        try:
            start = time.perf_counter()
            ticker = _yf.Ticker("^NSEI")
            _ = ticker.fast_info
            latency_ms = (time.perf_counter() - start) * 1000
            return ProviderHealth(
                provider_name=self.provider_name,
                status=ProviderStatus.HEALTHY,
                latency_ms=round(latency_ms, 2),
                message="Yahoo Finance reachable.",
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
        """Yahoo Finance does not provide an instrument catalog API.

        Returns a minimal hardcoded list of major NSE instruments that are
        always available. Real instrument management requires a broker adapter.
        """
        instruments = [
            InstrumentRecord(
                symbol="NIFTY",
                exchange="NSE",
                segment="INDEX",
                instrument_type="INDEX",
                display_name="NIFTY 50",
                lot_size=50,
                tick_size=Decimal("0.05"),
                trading_symbol="^NSEI",
            ),
            InstrumentRecord(
                symbol="BANKNIFTY",
                exchange="NSE",
                segment="INDEX",
                instrument_type="INDEX",
                display_name="BANK NIFTY",
                lot_size=15,
                tick_size=Decimal("0.05"),
                trading_symbol="^NSEBANK",
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
                trading_symbol="RELIANCE.NS",
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
                trading_symbol="HDFCBANK.NS",
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
                trading_symbol="TCS.NS",
            ),
        ]

        if exchange:
            instruments = [i for i in instruments if i.exchange == exchange.upper()]
        if segment:
            instruments = [i for i in instruments if i.segment == segment.upper()]
        return instruments

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
        self._require_yfinance()
        yf_symbol = self._yahoo_symbol(symbol, exchange)
        yf_interval = _TIMEFRAME_MAP.get(timeframe)
        if yf_interval is None:
            raise ProviderUnavailable(
                self.provider_name,
                f"Unsupported timeframe: '{timeframe}'",
            )

        try:
            ticker = _yf.Ticker(yf_symbol)
            df = ticker.history(
                start=from_dt.strftime("%Y-%m-%d"),
                end=to_dt.strftime("%Y-%m-%d"),
                interval=yf_interval,
                auto_adjust=True,
            )
        except Exception as exc:
            raise ProviderUnavailable(
                self.provider_name, f"yfinance error: {exc}"
            ) from exc

        if df.empty:
            return []

        records: list[OHLCVRecord] = []
        for ts, row in df.iterrows():
            # yfinance timestamps are tz-aware; coerce to UTC
            if hasattr(ts, "tzinfo") and ts.tzinfo is not None:
                ts_utc = ts.to_pydatetime().astimezone(timezone.utc)
            else:
                ts_utc = ts.to_pydatetime().replace(tzinfo=timezone.utc)

            records.append(
                OHLCVRecord(
                    symbol=symbol.upper(),
                    exchange=exchange.upper(),
                    timeframe=timeframe,
                    timestamp=ts_utc,
                    open=_dec(float(row["Open"])),
                    high=_dec(float(row["High"])),
                    low=_dec(float(row["Low"])),
                    close=_dec(float(row["Close"])),
                    volume=int(row.get("Volume", 0)),
                )
            )

        return records

    # ------------------------------------------------------------------
    # Live Quotes
    # ------------------------------------------------------------------

    def get_live_quote(self, symbol: str, exchange: str) -> LiveQuoteRecord:
        self._require_yfinance()
        yf_symbol = self._yahoo_symbol(symbol, exchange)
        try:
            ticker = _yf.Ticker(yf_symbol)
            info = ticker.fast_info
            last = float(info.last_price or 0)
            prev_close = float(info.previous_close or last)
            change = _dec(last - prev_close)
            change_pct = (
                _dec((last - prev_close) / prev_close * 100)
                if prev_close
                else Decimal("0")
            )
            return LiveQuoteRecord(
                symbol=symbol.upper(),
                exchange=exchange.upper(),
                last_price=_dec(last),
                bid=_dec(float(info.bid or last)),
                ask=_dec(float(info.ask or last)),
                high=_dec(float(info.day_high or last)),
                low=_dec(float(info.day_low or last)),
                open=_dec(float(info.open or last)),
                prev_close=_dec(prev_close),
                volume=int(info.three_month_average_volume or 0),
                timestamp=datetime.now(tz=timezone.utc),
                change=change,
                change_pct=change_pct,
            )
        except Exception as exc:
            raise ProviderUnavailable(
                self.provider_name, f"yfinance quote error: {exc}"
            ) from exc

    def get_live_quotes(
        self, symbols: list[tuple[str, str]]
    ) -> list[LiveQuoteRecord]:
        results: list[LiveQuoteRecord] = []
        for sym, exch in symbols:
            try:
                results.append(self.get_live_quote(sym, exch))
            except ProviderUnavailable:
                pass  # Skip failed symbols; caller receives partial results
        return results
