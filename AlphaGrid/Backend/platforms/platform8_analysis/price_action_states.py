from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, List
from Backend.core.state import BaseState, StateLifecycle, ExecutionContext

@dataclass
class CandlestickInputDTO:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

@dataclass
class CandlestickState(BaseState):
    body_size: float = 0.0
    upper_wick: float = 0.0
    lower_wick: float = 0.0
    is_bullish: bool = False
    is_bearish: bool = False
    
    @classmethod
    def calculate_next(cls, previous_state: Optional['CandlestickState'], input_dto: CandlestickInputDTO, context: ExecutionContext) -> 'CandlestickState':
        ver = 1 if previous_state is None else previous_state.version + 1
        lifecycle = StateLifecycle.CREATED if previous_state is None else StateLifecycle.UPDATED
        
        body_size = abs(input_dto.close - input_dto.open)
        upper_wick = input_dto.high - max(input_dto.open, input_dto.close)
        lower_wick = min(input_dto.open, input_dto.close) - input_dto.low
        
        return cls(
            context=context,
            lifecycle=lifecycle,
            timestamp=input_dto.timestamp,
            version=ver,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            body_size=body_size,
            upper_wick=upper_wick,
            lower_wick=lower_wick,
            is_bullish=input_dto.close > input_dto.open,
            is_bearish=input_dto.close < input_dto.open
        )

    def serialize(self) -> dict: return {}
    @classmethod
    def deserialize(cls, data: dict) -> 'CandlestickState': pass

@dataclass
class EngulfingState(BaseState):
    is_bullish_engulfing: bool = False
    is_bearish_engulfing: bool = False
    prev_open: float = 0.0
    prev_close: float = 0.0
    
    @classmethod
    def calculate_next(cls, previous_state: Optional['EngulfingState'], input_dto: CandlestickInputDTO, context: ExecutionContext) -> 'EngulfingState':
        ver = 1 if previous_state is None else previous_state.version + 1
        lifecycle = StateLifecycle.CREATED if previous_state is None else StateLifecycle.UPDATED
        
        is_bullish_eng = False
        is_bearish_eng = False
        
        if previous_state and previous_state.prev_open != 0:
            prev_bullish = previous_state.prev_close > previous_state.prev_open
            prev_bearish = previous_state.prev_close < previous_state.prev_open
            
            curr_bullish = input_dto.close > input_dto.open
            curr_bearish = input_dto.close < input_dto.open
            
            if prev_bearish and curr_bullish and input_dto.close > previous_state.prev_open and input_dto.open < previous_state.prev_close:
                is_bullish_eng = True
                
            if prev_bullish and curr_bearish and input_dto.close < previous_state.prev_open and input_dto.open > previous_state.prev_close:
                is_bearish_eng = True
        
        return cls(
            context=context,
            lifecycle=lifecycle,
            timestamp=input_dto.timestamp,
            version=ver,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            is_bullish_engulfing=is_bullish_eng,
            is_bearish_engulfing=is_bearish_eng,
            prev_open=input_dto.open,
            prev_close=input_dto.close
        )
        
    def serialize(self) -> dict: return {}
    @classmethod
    def deserialize(cls, data: dict) -> 'EngulfingState': pass

@dataclass
class PinBarState(BaseState):
    is_bullish_pinbar: bool = False
    is_bearish_pinbar: bool = False
    
    @classmethod
    def calculate_next(cls, previous_state: Optional['PinBarState'], input_dto: CandlestickInputDTO, context: ExecutionContext) -> 'PinBarState':
        ver = 1 if previous_state is None else previous_state.version + 1
        lifecycle = StateLifecycle.CREATED if previous_state is None else StateLifecycle.UPDATED
        
        body_size = abs(input_dto.close - input_dto.open)
        upper_wick = input_dto.high - max(input_dto.open, input_dto.close)
        lower_wick = min(input_dto.open, input_dto.close) - input_dto.low
        total_size = input_dto.high - input_dto.low
        
        is_bullish_pin = False
        is_bearish_pin = False
        
        if total_size > 0:
            if lower_wick > body_size * 2 and upper_wick < body_size:
                is_bullish_pin = True
            if upper_wick > body_size * 2 and lower_wick < body_size:
                is_bearish_pin = True
        
        return cls(
            context=context,
            lifecycle=lifecycle,
            timestamp=input_dto.timestamp,
            version=ver,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            is_bullish_pinbar=is_bullish_pin,
            is_bearish_pinbar=is_bearish_pin
        )
        
    def serialize(self) -> dict: return {}
    @classmethod
    def deserialize(cls, data: dict) -> 'PinBarState': pass

@dataclass
class InsideOutsideBarState(BaseState):
    is_inside_bar: bool = False
    is_outside_bar: bool = False
    prev_high: float = 0.0
    prev_low: float = 0.0
    
    @classmethod
    def calculate_next(cls, previous_state: Optional['InsideOutsideBarState'], input_dto: CandlestickInputDTO, context: ExecutionContext) -> 'InsideOutsideBarState':
        ver = 1 if previous_state is None else previous_state.version + 1
        lifecycle = StateLifecycle.CREATED if previous_state is None else StateLifecycle.UPDATED
        
        is_inside = False
        is_outside = False
        
        if previous_state and previous_state.prev_high != 0:
            if input_dto.high < previous_state.prev_high and input_dto.low > previous_state.prev_low:
                is_inside = True
            elif input_dto.high > previous_state.prev_high and input_dto.low < previous_state.prev_low:
                is_outside = True
        
        return cls(
            context=context,
            lifecycle=lifecycle,
            timestamp=input_dto.timestamp,
            version=ver,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            is_inside_bar=is_inside,
            is_outside_bar=is_outside,
            prev_high=input_dto.high,
            prev_low=input_dto.low
        )
        
    def serialize(self) -> dict: return {}
    @classmethod
    def deserialize(cls, data: dict) -> 'InsideOutsideBarState': pass

@dataclass
class MarubozuDojiState(BaseState):
    is_marubozu: bool = False
    is_doji: bool = False
    
    @classmethod
    def calculate_next(cls, previous_state: Optional['MarubozuDojiState'], input_dto: CandlestickInputDTO, context: ExecutionContext) -> 'MarubozuDojiState':
        ver = 1 if previous_state is None else previous_state.version + 1
        lifecycle = StateLifecycle.CREATED if previous_state is None else StateLifecycle.UPDATED
        
        body_size = abs(input_dto.close - input_dto.open)
        upper_wick = input_dto.high - max(input_dto.open, input_dto.close)
        lower_wick = min(input_dto.open, input_dto.close) - input_dto.low
        total_size = input_dto.high - input_dto.low
        
        is_mar = False
        is_doj = False
        
        if total_size > 0:
            if upper_wick < total_size * 0.05 and lower_wick < total_size * 0.05:
                is_mar = True
            if body_size < total_size * 0.1 and total_size > 0:
                is_doj = True
        
        return cls(
            context=context,
            lifecycle=lifecycle,
            timestamp=input_dto.timestamp,
            version=ver,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            is_marubozu=is_mar,
            is_doji=is_doj
        )
        
    def serialize(self) -> dict: return {}
    @classmethod
    def deserialize(cls, data: dict) -> 'MarubozuDojiState': pass
