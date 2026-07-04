from dataclasses import dataclass

@dataclass(frozen=True)
class MarketBar:
    """Immutable contract representing a single time-based OHLCV bar."""
    timestamp: int
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    timeframe: str
