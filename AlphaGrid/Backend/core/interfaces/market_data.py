from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterator, Any, Generic, TypeVar

# --- Time Semantics ---
@dataclass(frozen=True)
class TemporalContext:
    """Provides deterministic time semantics for all market primitives."""
    event_time: float      # When it actually occurred in the real world
    exchange_time: float   # When the exchange engine matched it
    receive_time: float    # When our gateway recorded it
    replay_time: float     # Simulation time (if running in backtest)

# --- Market Primitives ---
@dataclass(frozen=True)
class MarketPrimitive(ABC):
    symbol: str
    temporal_context: TemporalContext

@dataclass(frozen=True)
class Bar(MarketPrimitive):
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float

@dataclass(frozen=True)
class Tick(MarketPrimitive):
    price: float
    size: float

@dataclass(frozen=True)
class Quote(MarketPrimitive):
    bid_price: float
    bid_size: float
    ask_price: float
    ask_size: float

@dataclass(frozen=True)
class Trade(Tick):
    is_buyer_maker: bool

@dataclass(frozen=True)
class OrderBookSnapshot(MarketPrimitive):
    bids: list # List of price/size levels
    asks: list

@dataclass(frozen=True)
class MarketDepth(MarketPrimitive):
    depth_levels: int

@dataclass(frozen=True)
class CorporateAction(MarketPrimitive):
    action_type: str
    adjustment_factor: float

@dataclass(frozen=True)
class EconomicEvent(MarketPrimitive):
    event_name: str
    actual_value: float
    forecast_value: float
    previous_value: float

@dataclass(frozen=True)
class TradingSession(MarketPrimitive):
    session_name: str
    is_open: bool

@dataclass(frozen=True)
class InstrumentMetadata(MarketPrimitive):
    tick_size: float
    contract_multiplier: float
    currency: str

# --- Storage Abstraction Views ---
T = TypeVar('T', bound=MarketPrimitive)

class MarketDataView(ABC, Generic[T]):
    """
    Abstract read-only interface shielding engines from the underlying collection 
    (e.g., Python lists, NumPy arrays, Polars DataFrames).
    """
    
    @abstractmethod
    def latest(self) -> T:
        """Returns the most recent primitive."""
        pass
        
    @abstractmethod
    def previous(self, n: int = 1) -> T:
        """Returns the nth previous primitive."""
        pass
        
    @abstractmethod
    def window(self, size: int) -> 'MarketDataView[T]':
        """Returns a fixed-size rolling window view."""
        pass
        
    @abstractmethod
    def slice(self, start_idx: int, end_idx: int) -> 'MarketDataView[T]':
        """Returns a discrete slice of the view."""
        pass

    @abstractmethod
    def lookback(self, seconds: float) -> 'MarketDataView[T]':
        """Returns a time-based window view."""
        pass

    @abstractmethod
    def iterator(self) -> Iterator[T]:
        """Provides forward iteration capability without exposing the collection."""
        pass
        
    @abstractmethod
    def __len__(self) -> int:
        pass

class BarView(MarketDataView[Bar]):
    pass

class TickView(MarketDataView[Tick]):
    pass
