import pytest
import numpy as np

from Backend.math.public.sma import SMAState, update_sma
from Backend.core.dtos import OHLCV

def generate_feed(size=100):
    np.random.seed(42)
    prices = np.random.lognormal(mean=0.001, sigma=0.02, size=size)
    prices = np.cumprod(prices) * 100
    return [OHLCV(timestamp=i, open=p, high=p, low=p, close=p, volume=100, symbol="NIFTY") for i, p in enumerate(prices)]

def extract_snapshot(state: SMAState) -> dict:
    """Simulates serialization to the Snapshot Manager / Redis"""
    return {
        "period": state.period,
        "window_sum": float(state.window_sum),
        "window": list(state.window)
    }

def restore_snapshot(snapshot: dict) -> SMAState:
    """Simulates deserialization and hot-restart"""
    state = SMAState(period=snapshot["period"])
    state.window_sum = snapshot["window_sum"]
    # Re-hydrate the deque window
    for v in snapshot["window"]:
        state.window.append(v)
    return state

def test_snapshot_hot_restart_gate_5():
    """
    Gate 5: Snapshot Recovery
    Proves that taking a state snapshot halfway, killing the process, 
    restoring it into a new object, and continuing yields the EXACT 
    same mathematical outputs as an uninterrupted run.
    """
    feed = generate_feed(100)
    
    # --- 1. Continuous (Uninterrupted) Run ---
    uninterrupted_state = SMAState(period=14)
    continuous_results = []
    
    for bar in feed:
        val = update_sma(bar.close, uninterrupted_state)
        continuous_results.append(val)
        
    # --- 2. Snapshotted Run ---
    snapshot_results = []
    
    # Run the first 50 bars
    initial_state = SMAState(period=14)
    for bar in feed[:50]:
        val = update_sma(bar.close, initial_state)
        snapshot_results.append(val)
        
    # TAKE SNAPSHOT
    snapshot_data = extract_snapshot(initial_state)
    
    # 'KILL PROCESS'
    del initial_state
    
    # 'RESTART AND RESTORE'
    restored_state = restore_snapshot(snapshot_data)
    
    # Run the remaining 50 bars
    for bar in feed[50:]:
        val = update_sma(bar.close, restored_state)
        snapshot_results.append(val)
        
    # --- 3. Validate ---
    # Convert to Numpy Arrays for strict IEEE-754 float validation
    continuous_arr = np.array(continuous_results, dtype=np.float64)
    snapshot_arr = np.array(snapshot_results, dtype=np.float64)
    
    # Assert exact match (NaN-aware)
    np.testing.assert_array_equal(continuous_arr, snapshot_arr)
