import pytest
import time
import uuid
import numpy as np

from Backend.core.event_replay_validator import EventReplayValidator
from Backend.math.public.sma import SMAState, update_sma
from Backend.core.dtos import OHLCV

def generate_market_feed(size=50):
    """Generates a deterministic sequence of market bars"""
    np.random.seed(42)
    prices = np.random.lognormal(mean=0.001, sigma=0.02, size=size)
    prices = np.cumprod(prices) * 100
    
    feed = []
    base_time = int(time.time())
    for i, p in enumerate(prices):
        feed.append(OHLCV(
            timestamp=base_time + (i * 60), # 1 min bars
            open=p * 0.99,
            high=p * 1.02,
            low=p * 0.98,
            close=p,
            volume=1000,
            symbol="NIFTY"
        ))
    return feed

def extract_state_dict(state: SMAState) -> dict:
    """Helper to convert the raw state object to a dictionary for hashing"""
    return {
        "period": state.period,
        "window_sum": float(state.window_sum),
        "window": list(state.window),
        "count": len(state.window)
    }

def test_replay_determinism_gate_1():
    """
    Gate 1: Replay Determinism
    Proves that running an engine in "Live" mode generates 
    exact state hashes as running it in "Replay" mode.
    """
    feed = generate_market_feed(50)
    validator = EventReplayValidator()
    capability_id = f"SMA_14_{uuid.uuid4().hex[:8]}"
    
    # --- 1. LIVE EXECUTION ---
    live_state = SMAState(period=14)
    
    for bar in feed:
        # 1. Update State
        update_sma(bar.close, live_state)
        # 2. Record Hash in Validator
        state_dict = extract_state_dict(live_state)
        validator.record_live_state(str(bar.timestamp), capability_id, state_dict)
        
    # --- 2. SYSTEM RESTART / REPLAY ---
    # (Simulated by initializing a fresh state and replaying the same feed)
    replay_state = SMAState(period=14)
    
    for bar in feed:
        # 1. Update Replay State
        update_sma(bar.close, replay_state)
        # 2. Validate against Live Hash
        replay_dict = extract_state_dict(replay_state)
        
        is_deterministic = validator.validate_replay_state(str(bar.timestamp), capability_id, replay_dict)
        assert is_deterministic, f"DETERMINISM BROKEN at {bar.timestamp}: Live Hash != Replay Hash"
        
    report = validator.get_validation_report()
    assert report["is_deterministic"] is True
    assert report["total_validated"] == 50
    assert report["mismatches_found"] == 0
