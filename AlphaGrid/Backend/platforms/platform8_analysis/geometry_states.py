from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Any, Dict, List
from Backend.core.state import BaseState, StateLifecycle, ExecutionContext

@dataclass
class GeometryInputDTO:
    timestamp: datetime
    price: float
    high: float
    low: float
    volume: float

@dataclass
class SwingPoint:
    timestamp: datetime
    price: float
    type: str # "HIGH" or "LOW"
    confirmed: bool = False

@dataclass
class SwingState(BaseState):
    latest_swing_high: Optional[SwingPoint] = None
    latest_swing_low: Optional[SwingPoint] = None
    historical_swings: List[SwingPoint] = field(default_factory=list)
    window_highs: List[float] = field(default_factory=list)
    window_lows: List[float] = field(default_factory=list)
    window_timestamps: List[datetime] = field(default_factory=list)
    
    @classmethod
    def calculate_next(cls, previous_state: Optional['SwingState'], input_dto: GeometryInputDTO, context: ExecutionContext) -> 'SwingState':
        ver = 1 if previous_state is None else previous_state.version + 1
        lifecycle = StateLifecycle.CREATED if previous_state is None else StateLifecycle.UPDATED
        
        # Load previous history
        w_highs = list(previous_state.window_highs) if previous_state else []
        w_lows = list(previous_state.window_lows) if previous_state else []
        w_times = list(previous_state.window_timestamps) if previous_state else []
        hist_swings = list(previous_state.historical_swings) if previous_state else []
        
        last_high = previous_state.latest_swing_high if previous_state else None
        last_low = previous_state.latest_swing_low if previous_state else None

        # Add current bar
        w_highs.append(input_dto.high)
        w_lows.append(input_dto.low)
        w_times.append(input_dto.timestamp)
        
        # Maintain window of 5 (2 left, 1 center, 2 right)
        if len(w_highs) > 5:
            w_highs.pop(0)
            w_lows.pop(0)
            w_times.pop(0)
            
        # Detect swing high (Center is highest of 5)
        if len(w_highs) == 5:
            center_high = w_highs[2]
            if all(center_high > w_highs[i] for i in [0, 1, 3, 4]):
                new_swing_high = SwingPoint(timestamp=w_times[2], price=center_high, type="HIGH", confirmed=True)
                # Only add if it's new
                if not last_high or last_high.timestamp != new_swing_high.timestamp:
                    last_high = new_swing_high
                    hist_swings.append(new_swing_high)
                    
            center_low = w_lows[2]
            if all(center_low < w_lows[i] for i in [0, 1, 3, 4]):
                new_swing_low = SwingPoint(timestamp=w_times[2], price=center_low, type="LOW", confirmed=True)
                if not last_low or last_low.timestamp != new_swing_low.timestamp:
                    last_low = new_swing_low
                    hist_swings.append(new_swing_low)
                    
        # Cap historical swings
        if len(hist_swings) > 20:
            hist_swings = hist_swings[-20:]
        
        return cls(
            context=context,
            lifecycle=lifecycle,
            timestamp=input_dto.timestamp,
            version=ver,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            latest_swing_high=last_high,
            latest_swing_low=last_low,
            historical_swings=hist_swings,
            window_highs=w_highs,
            window_lows=w_lows,
            window_timestamps=w_times
        )

    def serialize(self) -> dict:
        return {}

    @classmethod
    def deserialize(cls, data: dict) -> 'SwingState':
        pass

@dataclass
class TimeExtremesState(BaseState):
    pdh: float = 0.0 # Previous Day High
    pdl: float = 0.0 # Previous Day Low
    pwh: float = 0.0 # Previous Week High
    pwl: float = 0.0 # Previous Week Low
    current_day_high: float = 0.0
    current_day_low: float = float('inf')
    current_day: int = -1
    
    @classmethod
    def calculate_next(cls, previous_state: Optional['TimeExtremesState'], input_dto: GeometryInputDTO, context: ExecutionContext) -> 'TimeExtremesState':
        ver = 1 if previous_state is None else previous_state.version + 1
        lifecycle = StateLifecycle.CREATED if previous_state is None else StateLifecycle.UPDATED
        
        pdh = previous_state.pdh if previous_state else input_dto.high
        pdl = previous_state.pdl if previous_state else input_dto.low
        cdh = previous_state.current_day_high if previous_state else input_dto.high
        cdl = previous_state.current_day_low if previous_state else input_dto.low
        cd = previous_state.current_day if previous_state else input_dto.timestamp.day
        
        # Rollover check
        if input_dto.timestamp.day != cd:
            pdh = cdh
            pdl = cdl
            cdh = input_dto.high
            cdl = input_dto.low
            cd = input_dto.timestamp.day
        else:
            cdh = max(cdh, input_dto.high)
            cdl = min(cdl, input_dto.low)
        
        return cls(
            context=context,
            lifecycle=lifecycle,
            timestamp=input_dto.timestamp,
            version=ver,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            pdh=pdh,
            pdl=pdl,
            pwh=previous_state.pwh if previous_state else input_dto.high, # Simplified for MVP
            pwl=previous_state.pwl if previous_state else input_dto.low,
            current_day_high=cdh,
            current_day_low=cdl,
            current_day=cd
        )

    def serialize(self) -> dict:
        return {}

    @classmethod
    def deserialize(cls, data: dict) -> 'TimeExtremesState':
        pass

@dataclass
class RangeState(BaseState):
    in_range: bool = False
    range_high: float = 0.0
    range_low: float = 0.0
    # Add dependency on swings
    consumes: List[str] = field(default_factory=lambda: ["SwingState"])
    
    @classmethod
    def calculate_next(cls, previous_state: Optional['RangeState'], input_dto: GeometryInputDTO, context: ExecutionContext) -> 'RangeState':
        ver = 1 if previous_state is None else previous_state.version + 1
        lifecycle = StateLifecycle.CREATED if previous_state is None else StateLifecycle.UPDATED
        
        # MVP: A range is detected if price is trapped between the last confirmed swing high and low.
        return cls(
            context=context,
            lifecycle=lifecycle,
            timestamp=input_dto.timestamp,
            version=ver,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            in_range=False,
            range_high=0.0,
            range_low=0.0
        )

    def serialize(self) -> dict:
        return {}

    @classmethod
    def deserialize(cls, data: dict) -> 'RangeState':
        pass

@dataclass
class SupportResistanceLevel:
    price: float
    strength: int = 1
    type: str = "SUPPORT"

@dataclass
class SupportResistanceState(BaseState):
    active_levels: List[SupportResistanceLevel] = field(default_factory=list)
    consumes: List[str] = field(default_factory=lambda: ["SwingState"])
    
    @classmethod
    def calculate_next(cls, previous_state: Optional['SupportResistanceState'], input_dto: GeometryInputDTO, context: ExecutionContext) -> 'SupportResistanceState':
        ver = 1 if previous_state is None else previous_state.version + 1
        lifecycle = StateLifecycle.CREATED if previous_state is None else StateLifecycle.UPDATED
        
        return cls(
            context=context,
            lifecycle=lifecycle,
            timestamp=input_dto.timestamp,
            version=ver,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            active_levels=previous_state.active_levels if previous_state else []
        )
        
    def serialize(self) -> dict:
        return {}

    @classmethod
    def deserialize(cls, data: dict) -> 'SupportResistanceState':
        pass

@dataclass
class TrendlineState(BaseState):
    active_trendlines: List[dict] = field(default_factory=list)
    consumes: List[str] = field(default_factory=lambda: ["SwingState"])
    
    @classmethod
    def calculate_next(cls, previous_state: Optional['TrendlineState'], input_dto: GeometryInputDTO, context: ExecutionContext) -> 'TrendlineState':
        ver = 1 if previous_state is None else previous_state.version + 1
        lifecycle = StateLifecycle.CREATED if previous_state is None else StateLifecycle.UPDATED
        
        return cls(
            context=context,
            lifecycle=lifecycle,
            timestamp=input_dto.timestamp,
            version=ver,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            active_trendlines=previous_state.active_trendlines if previous_state else []
        )
        
    def serialize(self) -> dict:
        return {}

    @classmethod
    def deserialize(cls, data: dict) -> 'TrendlineState':
        pass

@dataclass
class ChannelState(BaseState):
    active_channels: List[dict] = field(default_factory=list)
    consumes: List[str] = field(default_factory=lambda: ["TrendlineState"])
    
    @classmethod
    def calculate_next(cls, previous_state: Optional['ChannelState'], input_dto: GeometryInputDTO, context: ExecutionContext) -> 'ChannelState':
        ver = 1 if previous_state is None else previous_state.version + 1
        lifecycle = StateLifecycle.CREATED if previous_state is None else StateLifecycle.UPDATED
        
        return cls(
            context=context,
            lifecycle=lifecycle,
            timestamp=input_dto.timestamp,
            version=ver,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            active_channels=previous_state.active_channels if previous_state else []
        )
        
    def serialize(self) -> dict:
        return {}

    @classmethod
    def deserialize(cls, data: dict) -> 'ChannelState':
        pass

@dataclass
class CompressionExpansionState(BaseState):
    is_compressing: bool = False
    is_expanding: bool = False
    
    @classmethod
    def calculate_next(cls, previous_state: Optional['CompressionExpansionState'], input_dto: GeometryInputDTO, context: ExecutionContext) -> 'CompressionExpansionState':
        ver = 1 if previous_state is None else previous_state.version + 1
        lifecycle = StateLifecycle.CREATED if previous_state is None else StateLifecycle.UPDATED
        
        return cls(
            context=context,
            lifecycle=lifecycle,
            timestamp=input_dto.timestamp,
            version=ver,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            is_compressing=False,
            is_expanding=False
        )
        
    def serialize(self) -> dict:
        return {}

    @classmethod
    def deserialize(cls, data: dict) -> 'CompressionExpansionState':
        pass
