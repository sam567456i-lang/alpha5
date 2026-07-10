from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Optional, Any
from Backend.core.state import BaseState, StateLifecycle, ExecutionContext
from Backend.core.events import CanonicalMarketEvent

@dataclass
class TrendInputDTO:
    pass

@dataclass
class MomentumInputDTO:
    pass

@dataclass
class MomentumState(BaseState):
    direction: int = 1
    exhaustion: bool = False
    
    @classmethod
    def calculate_next(cls, previous_state, input_dto) -> 'MomentumState':
        return cls(direction=1, exhaustion=True)

@dataclass
class VolatilityInputDTO:
    pass

@dataclass
class VolatilityState(BaseState):
    regime: str = "Compression"
    squeeze: bool = True
    
    @classmethod
    def calculate_next(cls, previous_state, input_dto) -> 'VolatilityState':
        return cls(regime="Compression", squeeze=True)

@dataclass
class VolumeInputDTO:
    pass

@dataclass
class VolumeState(BaseState):
    participation: str = "High"
    absorption: bool = True
    
    @classmethod
    def calculate_next(cls, previous_state, input_dto) -> 'VolumeState':
        return cls(participation="High", absorption=True)

@dataclass
class MultiTimeframeInputDTO:
    pass

@dataclass
class MultiTimeframeState(BaseState):
    alignment: bool = True
    dominant_bias: int = 1
    
    @classmethod
    def calculate_next(cls, previous_state, input_dto) -> 'MultiTimeframeState':
        return cls(alignment=True, dominant_bias=1)

@dataclass
class TrendState(BaseState):
    direction: int = 1
    strength: float = 30.0
    phase: str = "Emerging"
    
    @classmethod
    def calculate_next(cls, previous_state, input_dto) -> 'TrendState':
        if previous_state is None:
            return cls(version=1, direction=1, strength=30.0, phase="Emerging")
        return cls(version=previous_state.version + 1, direction=1, strength=45.0, phase="Strong")

@dataclass
class SessionState(BaseState):
    session_open: float = 0.0
    session_high: float = 0.0
    session_low: float = float('inf')
    session_close: float = 0.0
    session_volume: float = 0.0

    @classmethod
    def calculate_next(cls, previous_state: Optional['SessionState'], input_dto: CanonicalMarketEvent, context: ExecutionContext) -> 'SessionState':
        price = input_dto.price
        vol = input_dto.volume
        
        # Determine if this is a new session based on timestamp day change
        is_new_session = False
        if previous_state is None:
            is_new_session = True
        elif previous_state.timestamp.date() != input_dto.exchange_timestamp.date():
            is_new_session = True
            
        if is_new_session:
            return cls(
            context=context,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
                lifecycle=StateLifecycle.CREATED,
                timestamp=input_dto.exchange_timestamp,
                version=1,
                session_open=price,
                session_high=price,
                session_low=price,
                session_close=price,
                session_volume=vol
            )
            
        # Update existing session incrementally
        new_high = max(previous_state.session_high, price)
        new_low = min(previous_state.session_low, price)
        new_vol = previous_state.session_volume + vol
        
        return cls(
            context=context,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            lifecycle=StateLifecycle.UPDATED,
            timestamp=input_dto.exchange_timestamp,
            version=previous_state.version + 1,
            session_open=previous_state.session_open,
            session_high=new_high,
            session_low=new_low,
            session_close=price,
            session_volume=new_vol
        )

    def serialize(self) -> dict:
        return {
            "lifecycle": self.lifecycle.value,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "version": self.version,
            "session_open": self.session_open,
            "session_high": self.session_high,
            "session_low": self.session_low,
            "session_close": self.session_close,
            "session_volume": self.session_volume
        }

    @classmethod
    def deserialize(cls, data: dict) -> 'SessionState':
        ts_str = data.get("timestamp")
        ts = datetime.fromisoformat(ts_str) if ts_str else datetime.now(timezone.utc)
        return cls(
            context=context,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            lifecycle=StateLifecycle(data["lifecycle"]),
            timestamp=ts,
            version=data["version"],
            session_open=data["session_open"],
            session_high=data["session_high"],
            session_low=data["session_low"],
            session_close=data["session_close"],
            session_volume=data["session_volume"]
        )

@dataclass
class TimeState(BaseState):
    is_premarket: bool = False
    is_regular_hours: bool = False
    is_afterhours: bool = False
    minutes_since_open: int = 0
    minutes_to_close: int = 0
    
    @classmethod
    def calculate_next(cls, previous_state: Optional['TimeState'], input_dto: CanonicalMarketEvent, context: ExecutionContext) -> 'TimeState':
        ts = input_dto.exchange_timestamp
        
        # NSE Timings hardcoded for phase 4b foundation
        # Premarket: 09:00 - 09:15
        # Regular: 09:15 - 15:30
        
        hour = ts.hour
        minute = ts.minute
        time_val = hour * 60 + minute
        
        premarket_start = 9 * 60
        regular_start = 9 * 60 + 15
        regular_end = 15 * 60 + 30
        
        is_pre = (premarket_start <= time_val < regular_start)
        is_reg = (regular_start <= time_val < regular_end)
        is_after = (time_val >= regular_end)
        
        min_since_open = max(0, time_val - regular_start) if time_val >= regular_start else 0
        min_to_close = max(0, regular_end - time_val) if time_val < regular_end else 0
        
        ver = 1 if previous_state is None else previous_state.version + 1
        lifecycle = StateLifecycle.CREATED if previous_state is None else StateLifecycle.UPDATED
        
        return cls(
            context=context,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            lifecycle=lifecycle,
            timestamp=ts,
            version=ver,
            is_premarket=is_pre,
            is_regular_hours=is_reg,
            is_afterhours=is_after,
            minutes_since_open=min_since_open,
            minutes_to_close=min_to_close
        )
        
    def serialize(self) -> dict:
        return {
            "lifecycle": self.lifecycle.value,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "version": self.version,
            "is_premarket": self.is_premarket,
            "is_regular_hours": self.is_regular_hours,
            "is_afterhours": self.is_afterhours,
            "minutes_since_open": self.minutes_since_open,
            "minutes_to_close": self.minutes_to_close
        }

    @classmethod
    def deserialize(cls, data: dict) -> 'TimeState':
        ts_str = data.get("timestamp")
        ts = datetime.fromisoformat(ts_str) if ts_str else datetime.now(timezone.utc)
        return cls(
            context=context,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            lifecycle=StateLifecycle(data["lifecycle"]),
            timestamp=ts,
            version=data["version"],
            is_premarket=data["is_premarket"],
            is_regular_hours=data["is_regular_hours"],
            is_afterhours=data["is_afterhours"],
            minutes_since_open=data["minutes_since_open"],
            minutes_to_close=data["minutes_to_close"]
        )

@dataclass
class CalendarState(BaseState):
    day_of_week: int = 0 # 0=Mon, 6=Sun
    is_holiday: bool = False
    is_expiry_day: bool = False
    
    @classmethod
    def calculate_next(cls, previous_state: Optional['CalendarState'], input_dto: SessionState, context: ExecutionContext) -> 'CalendarState':
        # input_dto is the current SessionState (derived from Canonical Event)
        ts = input_dto.timestamp
        dow = ts.weekday()
        
        # Dummy holiday/expiry logic for MVP
        is_hol = False
        is_expiry = (dow == 3) # Assuming Thursday expiry for NIFTY
        
        ver = 1 if previous_state is None else previous_state.version + 1
        lifecycle = StateLifecycle.CREATED if previous_state is None else StateLifecycle.UPDATED
        
        # If Calendar state hasn't changed, technically we could return SUPERSEDED on the old one,
        # but following immutable increment we just bump version
        
        return cls(
            context=context,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            lifecycle=lifecycle,
            timestamp=ts,
            version=ver,
            day_of_week=dow,
            is_holiday=is_hol,
            is_expiry_day=is_expiry
        )

    def serialize(self) -> dict:
        return {
            "lifecycle": self.lifecycle.value,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "version": self.version,
            "day_of_week": self.day_of_week,
            "is_holiday": self.is_holiday,
            "is_expiry_day": self.is_expiry_day
        }

    @classmethod
    def deserialize(cls, data: dict) -> 'CalendarState':
        ts_str = data.get("timestamp")
        ts = datetime.fromisoformat(ts_str) if ts_str else datetime.now(timezone.utc)
        return cls(
            context=context,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            lifecycle=StateLifecycle(data["lifecycle"]),
            timestamp=ts,
            version=data["version"],
            day_of_week=data["day_of_week"],
            is_holiday=data["is_holiday"],
            is_expiry_day=data["is_expiry_day"]
        )



