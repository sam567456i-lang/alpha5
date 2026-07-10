from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from datetime import datetime

class DataContractException(Exception):
    pass

@dataclass(frozen=True)
class OHLCSchema:
    """Explicit data contract for an OHLC bar."""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    optional_fields: Dict[str, Any]

@dataclass(frozen=True)
class TickSchema:
    """Explicit data contract for raw tick data."""
    timestamp: datetime
    price: float
    size: float
    side: str # "BUY", "SELL", "UNKNOWN"

@dataclass(frozen=True)
class OrderBookSchema:
    """Explicit data contract for Level 2 order book updates."""
    timestamp: datetime
    bid_prices: List[float]
    bid_sizes: List[float]
    ask_prices: List[float]
    ask_sizes: List[float]
    depth: int
    sequence: int

class ContractValidator:
    """Validates raw data against the strict schemas before semantic validation."""
    
    @staticmethod
    def validate_ohlc(data: Dict[str, Any]) -> OHLCSchema:
        try:
            return OHLCSchema(
                timestamp=data["timestamp"],
                open=float(data["open"]),
                high=float(data["high"]),
                low=float(data["low"]),
                close=float(data["close"]),
                volume=float(data["volume"]),
                optional_fields=data.get("optional_fields", {})
            )
        except (KeyError, ValueError, TypeError) as e:
            raise DataContractException(f"Failed OHLC contract validation: {e}")
