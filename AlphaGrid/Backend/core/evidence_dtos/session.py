from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict
from datetime import time, date, datetime
from Backend.core.evidence_dtos.base import BasePlatformObject

class SessionBoundaryType(Enum):
    HIGH = "HIGH"
    LOW = "LOW"
    MID = "MID"
    RANGE = "RANGE"

@dataclass(frozen=True)
class SessionDefinition:
    """Declarative definition of a session."""
    id: str
    calendar: str
    timezone: str
    start: time
    end: time
    holidays: str
    dst: str
    enabled: bool

@dataclass(frozen=True)
class TradingDay:
    date: date
    is_holiday: bool
    is_half_day: bool
    active_sessions: List[str]

@dataclass(frozen=True)
class TradingCalendar:
    """Owns market schedules (holidays, weekends, DST)."""
    id: str
    timezone: str
    trading_days: Dict[date, TradingDay]

@dataclass(frozen=True)
class SessionWindow:
    """A specific instance of a session over a trading day."""
    session_id: str
    trading_day: date
    actual_start_time: datetime
    actual_end_time: datetime

@dataclass(frozen=True)
class SessionLiquidityEvidence:
    """Purely objective evidence for Session Liquidity."""
    session_id: str
    boundary_type: SessionBoundaryType
    price: float
    timestamp: datetime
    origin_bar_timestamp: datetime
    calendar_id: str
    window_start: datetime
    window_end: datetime

@dataclass
class SessionLiquidityObject(BasePlatformObject):
    """
    Aggregates Identity, Evidence, Quality, Snapshots, and Revisions.
    Inherits from BasePlatformObject.
    """
    evidence: Optional[SessionLiquidityEvidence] = None

    def touch(self, lifecycle_engine):
        from Backend.core.engines.lifecycle import LifecycleEvent
        lifecycle_engine.process_event(self, LifecycleEvent.TOUCH_REQUESTED)
        
    def break_level(self, lifecycle_engine):
        # Implementation left to liquidity events wave
        pass
        
    def consume(self, lifecycle_engine):
        from Backend.core.engines.lifecycle import LifecycleEvent
        lifecycle_engine.process_event(self, LifecycleEvent.CONSUME_REQUESTED)
