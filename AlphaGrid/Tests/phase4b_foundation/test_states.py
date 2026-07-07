import pytest
from datetime import datetime, timezone
from Backend.core.state import StateLifecycle
from Backend.market_foundation.states import (
    TrendInputDTO, TrendState,
    MomentumInputDTO, MomentumState,
    VolatilityInputDTO, VolatilityState,
    VolumeInputDTO, VolumeState,
    MultiTimeframeInputDTO, MultiTimeframeState
)

def test_trend_state_incremental():
    ts1 = datetime(2026, 7, 5, 10, 0, tzinfo=timezone.utc)
    # Fast > Slow -> Bullish
    dto1 = TrendInputDTO(timestamp=ts1, price=100.0, ema_fast=105.0, ema_slow=100.0, adx=30.0)
    
    state1 = TrendState.calculate_next(None, dto1)
    
    assert state1.lifecycle == StateLifecycle.CREATED
    assert state1.version == 1
    assert state1.direction == 1
    assert state1.strength == 30.0
    assert state1.phase == "Emerging"
    
    ts2 = datetime(2026, 7, 5, 10, 1, tzinfo=timezone.utc)
    dto2 = TrendInputDTO(timestamp=ts2, price=102.0, ema_fast=107.0, ema_slow=101.0, adx=45.0)
    
    state2 = TrendState.calculate_next(state1, dto2)
    
    assert state2.lifecycle == StateLifecycle.UPDATED
    assert state2.version == 2
    assert state2.direction == 1
    assert state2.strength == 45.0
    assert state2.phase == "Strong"

def test_momentum_state_exhaustion():
    ts1 = datetime(2026, 7, 5, 10, 0, tzinfo=timezone.utc)
    dto1 = MomentumInputDTO(timestamp=ts1, rsi=75.0, macd_hist=0.5, roc=1.2)
    
    state1 = MomentumState.calculate_next(None, dto1)
    
    assert state1.direction == 1
    assert state1.exhaustion is True

def test_volatility_state_compression():
    ts1 = datetime(2026, 7, 5, 10, 0, tzinfo=timezone.utc)
    dto1 = VolatilityInputDTO(timestamp=ts1, atr=0.5, bollinger_bandwidth=1.2)
    
    state1 = VolatilityState.calculate_next(None, dto1)
    
    assert state1.regime == "Compression"
    assert state1.squeeze is True

def test_volume_state_absorption():
    ts1 = datetime(2026, 7, 5, 10, 0, tzinfo=timezone.utc)
    # High relative volume and price exactly at VWAP
    dto1 = VolumeInputDTO(timestamp=ts1, volume=1000.0, relative_volume=2.0, price=100.0, vwap=100.0)
    
    state1 = VolumeState.calculate_next(None, dto1)
    
    assert state1.participation == "High"
    assert state1.absorption is True

def test_multitimeframe_alignment():
    ts1 = datetime(2026, 7, 5, 10, 0, tzinfo=timezone.utc)
    t1 = TrendState(lifecycle=StateLifecycle.CREATED, timestamp=ts1, version=1, direction=1, strength=30.0, phase="Emerging")
    t5 = TrendState(lifecycle=StateLifecycle.CREATED, timestamp=ts1, version=1, direction=1, strength=35.0, phase="Strong")
    t15 = TrendState(lifecycle=StateLifecycle.CREATED, timestamp=ts1, version=1, direction=1, strength=40.0, phase="Strong")
    
    dto1 = MultiTimeframeInputDTO(timestamp=ts1, trend_1m=t1, trend_5m=t5, trend_15m=t15)
    state1 = MultiTimeframeState.calculate_next(None, dto1)
    
    assert state1.alignment is True
    assert state1.dominant_bias == 1

def test_serialization_determinism():
    ts1 = datetime(2026, 7, 5, 10, 0, tzinfo=timezone.utc)
    dto1 = MomentumInputDTO(timestamp=ts1, rsi=75.0, macd_hist=0.5, roc=1.2)
    
    state1 = MomentumState.calculate_next(None, dto1)
    serialized = state1.serialize()
    
    assert serialized["lifecycle"] == "CREATED"
    assert serialized["direction"] == 1
    
    state2 = MomentumState.deserialize(serialized)
    assert state2.lifecycle == StateLifecycle.CREATED
    assert state2.direction == 1
    assert state2.timestamp == ts1
