import pytest
import numpy as np

from Backend.core.failure_isolation import FailureIsolationWrapper
from Backend.math.public.sma import SMAState, update_sma
from Backend.core.dtos import OHLCV

def mock_crashing_indicator(state: SMAState, bar: OHLCV):
    """Mocks a capability that intentionally raises a zero-division error occasionally"""
    if bar.timestamp == 5:
        return 1 / 0  # Crash on tick 5
    
    val = update_sma(bar.close, state)
    state.values = {'sma': val} # Mocking IncrementalState behavior
    return state

def mock_pipeline_engine():
    """Mocks the core event bus scheduler iterating over capabilities"""
    state = SMAState(period=3)
    state.values = {'sma': np.nan}
    
    results = []
    
    for i in range(10):
        bar = OHLCV(timestamp=i, open=100, high=100, low=100, close=100, volume=100, symbol="NIFTY")
        
        # Execute the wrapper safely
        safe_state = FailureIsolationWrapper.execute_safe(
            node_id="MOCK_CRASHER",
            capability_func=mock_crashing_indicator,
            state=state,
            new_bar=bar,
            fallback_value=np.nan
        )
        
        results.append((i, safe_state.values.get('sma', np.nan)))
        
    return results

def test_failure_isolation_gate_6():
    """
    Gate 6: Failure Isolation
    Proves that injecting a random exception (ZeroDivisionError) into a capability 
    DOES NOT crash the pipeline. The wrapper catches the exception, degrades the 
    output state to NaN (fallback_value), and allows the pipeline to continue.
    """
    
    # 1. Execute the mock pipeline which contains a guaranteed crash at tick 5
    results = mock_pipeline_engine()
    
    # 2. Assert Pipeline reached the end (10 ticks) despite the crash
    assert len(results) == 10, "Pipeline halted prematurely!"
    
    # 3. Assert Tick 5 (the crash) was safely degraded to NaN
    tick_5_result = results[5][1]
    assert np.isnan(tick_5_result), f"Tick 5 did not fallback to NaN, got {tick_5_result}"
    
    # 4. Assert Tick 6 (post-crash) successfully executed
    tick_6_result = results[6][1]
    assert not np.isnan(tick_6_result), "Pipeline failed to recover after crash!"
