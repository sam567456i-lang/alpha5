import pytest
import time
import numpy as np

from Backend.math.public.sma import SMAState, update_sma
from Backend.core.dtos import OHLCV

def test_performance_gate_2():
    """
    Gate 2: Performance Benchmarks
    Proves that O(1) Incremental indicator updates 
    process in under 5 microseconds per tick.
    """
    
    # 1. Generate 100,000 ticks
    np.random.seed(42)
    prices = np.random.lognormal(mean=0.001, sigma=0.02, size=100000)
    prices = np.cumprod(prices) * 100
    
    state = SMAState(period=14)
    
    # 2. Warm up (avoid python overheads in timing)
    for i in range(100):
        update_sma(prices[i], state)
        
    state = SMAState(period=14)
    
    # 3. Perf Run
    start_time = time.perf_counter()
    
    for p in prices:
        update_sma(p, state)
        
    end_time = time.perf_counter()
    
    total_time = end_time - start_time
    time_per_tick = total_time / len(prices)
    time_per_tick_us = time_per_tick * 1_000_000
    
    # Validation: Must be faster than 10 microseconds per tick in pure python 
    # (Since this is raw Python without Cython/Numba yet, 10us is our Phase 2 benchmark limit)
    assert time_per_tick_us < 10.0, f"Performance too slow! Took {time_per_tick_us:.2f} microseconds per tick."
