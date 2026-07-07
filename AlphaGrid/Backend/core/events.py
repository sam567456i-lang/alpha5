from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from Backend.dtos.provider import DataQualityScore
from Backend.dtos.instrument import InstrumentID

@dataclass(frozen=True)
class EventProvenance:
    trace_id: str
    event_id: str
    parent_event_id: Optional[str]
    origin_service: str
    origin_provider: str
    schema_version: int
    timestamp: datetime = field(default_factory=datetime.utcnow)
    is_replay: bool = False

class EventPriority:
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5

from Backend.shared_domain.contracts.dtos import LineageDTO

@dataclass(frozen=True)
class BaseEvent:
    provenance: EventProvenance
    priority: int = EventPriority.MEDIUM
    quality: Optional[DataQualityScore] = None
    lineage: Optional[LineageDTO] = None

@dataclass(frozen=True)
class CanonicalMarketEvent(BaseEvent):
    instrument_id: InstrumentID = None
    price: float = 0.0
    volume: float = 0.0
    exchange_timestamp: Optional[datetime] = None
    bid: Optional[float] = None
    ask: Optional[float] = None

@dataclass(frozen=True)
class DerivedMetrics:
    hl2: Optional[float] = None
    hlc3: Optional[float] = None
    ohlc4: Optional[float] = None
    typical_price: Optional[float] = None
    true_range: Optional[float] = None
    gap_percent: Optional[float] = None
    log_return: Optional[float] = None
    session_volume: Optional[float] = None

@dataclass(frozen=True)
class EnrichedMarketEvent(CanonicalMarketEvent):
    derived: DerivedMetrics = field(default_factory=DerivedMetrics)
