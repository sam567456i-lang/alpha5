from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, List
from Backend.core.state import BaseState, StateLifecycle, ExecutionContext
from Backend.platforms.platform8_analysis.geometry_states import SwingState
from Backend.platforms.platform8_analysis.liquidity_states import LiquidityState

@dataclass
class MarketStructureInputDTO:
    timestamp: datetime
    price: float
    high: float
    low: float
    close: float
    swing_state: Optional[SwingState] = None

@dataclass
class BreakOfStructureState(BaseState):
    is_bos: bool = False
    direction: str = "NONE" # BULLISH or BEARISH
    confirmed: bool = False
    consumes: List[str] = field(default_factory=lambda: ["SwingState"])
    
    @classmethod
    def calculate_next(cls, previous_state: Optional['BreakOfStructureState'], input_dto: MarketStructureInputDTO, context: ExecutionContext) -> 'BreakOfStructureState':
        ver = 1 if previous_state is None else previous_state.version + 1
        lifecycle = StateLifecycle.CREATED if previous_state is None else StateLifecycle.UPDATED
        
        is_bos = False
        dir_bos = "NONE"
        
        if input_dto.swing_state and len(input_dto.swing_state.historical_swings) > 0:
            last_high = next((s for s in reversed(input_dto.swing_state.historical_swings) if s.type == "HIGH"), None)
            last_low = next((s for s in reversed(input_dto.swing_state.historical_swings) if s.type == "LOW"), None)
            
            # Simple BOS logic MVP: Close above last major swing high
            if last_high and input_dto.close > last_high.price:
                is_bos = True
                dir_bos = "BULLISH"
            elif last_low and input_dto.close < last_low.price:
                is_bos = True
                dir_bos = "BEARISH"
        
        return cls(
            context=context,
            lifecycle=lifecycle,
            timestamp=input_dto.timestamp,
            version=ver,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            is_bos=is_bos,
            direction=dir_bos,
            confirmed=is_bos
        )
        
    def serialize(self) -> dict: return {}
    @classmethod
    def deserialize(cls, data: dict) -> 'BreakOfStructureState': pass

@dataclass
class ChangeOfCharacterState(BaseState):
    is_choch: bool = False
    direction: str = "NONE"
    consumes: List[str] = field(default_factory=lambda: ["SwingState"])
    
    @classmethod
    def calculate_next(cls, previous_state: Optional['ChangeOfCharacterState'], input_dto: MarketStructureInputDTO, context: ExecutionContext) -> 'ChangeOfCharacterState':
        ver = 1 if previous_state is None else previous_state.version + 1
        lifecycle = StateLifecycle.CREATED if previous_state is None else StateLifecycle.UPDATED
        
        return cls(
            context=context,
            lifecycle=lifecycle,
            timestamp=input_dto.timestamp,
            version=ver,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            is_choch=False,
            direction="NONE"
        )
        
    def serialize(self) -> dict: return {}
    @classmethod
    def deserialize(cls, data: dict) -> 'ChangeOfCharacterState': pass

@dataclass
class MarketStructureShiftState(BaseState):
    is_mss: bool = False
    direction: str = "NONE"
    consumes: List[str] = field(default_factory=lambda: ["SwingState"])
    
    @classmethod
    def calculate_next(cls, previous_state: Optional['MarketStructureShiftState'], input_dto: MarketStructureInputDTO, context: ExecutionContext) -> 'MarketStructureShiftState':
        ver = 1 if previous_state is None else previous_state.version + 1
        lifecycle = StateLifecycle.CREATED if previous_state is None else StateLifecycle.UPDATED
        
        return cls(
            context=context,
            lifecycle=lifecycle,
            timestamp=input_dto.timestamp,
            version=ver,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            is_mss=False,
            direction="NONE"
        )
        
    def serialize(self) -> dict: return {}
    @classmethod
    def deserialize(cls, data: dict) -> 'MarketStructureShiftState': pass

@dataclass
class InternalExternalStructureState(BaseState):
    internal_trend: str = "NEUTRAL"
    external_trend: str = "NEUTRAL"
    consumes: List[str] = field(default_factory=lambda: ["BreakOfStructureState"])
    
    @classmethod
    def calculate_next(cls, previous_state: Optional['InternalExternalStructureState'], input_dto: MarketStructureInputDTO, context: ExecutionContext) -> 'InternalExternalStructureState':
        ver = 1 if previous_state is None else previous_state.version + 1
        lifecycle = StateLifecycle.CREATED if previous_state is None else StateLifecycle.UPDATED
        
        return cls(
            context=context,
            lifecycle=lifecycle,
            timestamp=input_dto.timestamp,
            version=ver,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            internal_trend="NEUTRAL",
            external_trend="NEUTRAL"
        )
        
    def serialize(self) -> dict: return {}
    @classmethod
    def deserialize(cls, data: dict) -> 'InternalExternalStructureState': pass
