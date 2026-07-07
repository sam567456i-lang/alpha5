from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, List, Any
from Backend.core.state import BaseState, StateLifecycle, ExecutionContext
from Backend.platforms.platform8_analysis.geometry_states import SwingState, TimeExtremesState, SwingPoint

@dataclass
class LiquidityInputDTO:
    timestamp: datetime
    price: float
    high: float
    low: float
    volume: float
    swing_state: Optional[SwingState] = None

@dataclass
class LiquidityPool:
    price_level: float
    volume_at_level: float
    is_buyside: bool # Buy-side liquidity (above price)
    is_sellside: bool # Sell-side liquidity (below price)

@dataclass
class LiquidityState(BaseState):
    pools: List[LiquidityPool] = field(default_factory=list)
    internal_liquidity: float = 0.0
    external_liquidity: float = 0.0
    consumes: List[str] = field(default_factory=lambda: ["SwingState"])
    
    @classmethod
    def calculate_next(cls, previous_state: Optional['LiquidityState'], input_dto: LiquidityInputDTO, context: ExecutionContext) -> 'LiquidityState':
        ver = 1 if previous_state is None else previous_state.version + 1
        lifecycle = StateLifecycle.CREATED if previous_state is None else StateLifecycle.UPDATED
        
        pools = []
        if input_dto.swing_state:
            # Build pools based on historical unmitigated swings
            for swing in input_dto.swing_state.historical_swings:
                if swing.type == "HIGH":
                    pools.append(LiquidityPool(price_level=swing.price, volume_at_level=0, is_buyside=True, is_sellside=False))
                else:
                    pools.append(LiquidityPool(price_level=swing.price, volume_at_level=0, is_buyside=False, is_sellside=True))
                    
        return cls(
            context=context,
            lifecycle=lifecycle,
            timestamp=input_dto.timestamp,
            version=ver,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            pools=pools,
            internal_liquidity=0.0,
            external_liquidity=0.0
        )
        
    def serialize(self) -> dict: return {}
    @classmethod
    def deserialize(cls, data: dict) -> 'LiquidityState': pass

@dataclass
class SweepState(BaseState):
    is_sweeping_high: bool = False
    is_sweeping_low: bool = False
    swept_level: Optional[float] = None
    consumes: List[str] = field(default_factory=lambda: ["SwingState"])
    
    @classmethod
    def calculate_next(cls, previous_state: Optional['SweepState'], input_dto: LiquidityInputDTO, context: ExecutionContext) -> 'SweepState':
        ver = 1 if previous_state is None else previous_state.version + 1
        lifecycle = StateLifecycle.CREATED if previous_state is None else StateLifecycle.UPDATED
        
        is_sweep_high = False
        is_sweep_low = False
        swept = None
        
        if input_dto.swing_state and input_dto.swing_state.latest_swing_high:
            # Did price pierce the high but close below it? (Mock logic for MVP)
            if input_dto.high > input_dto.swing_state.latest_swing_high.price and input_dto.price < input_dto.swing_state.latest_swing_high.price:
                is_sweep_high = True
                swept = input_dto.swing_state.latest_swing_high.price
                
        if input_dto.swing_state and input_dto.swing_state.latest_swing_low:
            if input_dto.low < input_dto.swing_state.latest_swing_low.price and input_dto.price > input_dto.swing_state.latest_swing_low.price:
                is_sweep_low = True
                swept = input_dto.swing_state.latest_swing_low.price
        
        return cls(
            context=context,
            lifecycle=lifecycle,
            timestamp=input_dto.timestamp,
            version=ver,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            is_sweeping_high=is_sweep_high,
            is_sweeping_low=is_sweep_low,
            swept_level=swept
        )
        
    def serialize(self) -> dict: return {}
    @classmethod
    def deserialize(cls, data: dict) -> 'SweepState': pass

@dataclass
class StopHuntState(BaseState):
    is_stop_hunt: bool = False
    direction: str = "NONE" # "BULLISH", "BEARISH", "NONE"
    consumes: List[str] = field(default_factory=lambda: ["SweepState"])
    
    @classmethod
    def calculate_next(cls, previous_state: Optional['StopHuntState'], input_dto: LiquidityInputDTO, context: ExecutionContext) -> 'StopHuntState':
        ver = 1 if previous_state is None else previous_state.version + 1
        lifecycle = StateLifecycle.CREATED if previous_state is None else StateLifecycle.UPDATED
        
        return cls(
            context=context,
            lifecycle=lifecycle,
            timestamp=input_dto.timestamp,
            version=ver,
            created_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            updated_at=context.timestamp if hasattr(context, 'timestamp') else datetime.now(timezone.utc),
            is_stop_hunt=False,
            direction="NONE"
        )
        
    def serialize(self) -> dict: return {}
    @classmethod
    def deserialize(cls, data: dict) -> 'StopHuntState': pass
