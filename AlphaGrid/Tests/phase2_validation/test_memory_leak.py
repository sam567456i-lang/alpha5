import pytest
import tracemalloc
import gc
import numpy as np
from Backend.math.public.sma import SMAState, update_sma
from Backend.core.dtos import OHLCV

def test_memory_leak_gate_3():
    """
    Gate 3: Memory Leak Testing
    Simulates a continuous execution over 100,000 ticks.
    Proves that O(1) state memory footprint remains perfectly flat 
    and does not accumulate unbounded memory references.
    """
    state = SMAState(period=20)
    
    # 1. Warm-up Phase (to establish baseline after object allocations)
    for i in range(1000):
        bar = OHLCV(timestamp=i, open=100, high=100, low=100, close=100, volume=100, symbol="NIFTY")
        update_sma(bar.close, state)
        
    gc.collect()
    tracemalloc.start()
    
    # Snapshot at T=1000
    snapshot_start = tracemalloc.take_snapshot()
    
    # 2. Continuous Run Phase (Simulating Days/Weeks of execution)
    for i in range(1000, 100000):
        bar = OHLCV(timestamp=i, open=100, high=100, low=100, close=100, volume=100, symbol="NIFTY")
        update_sma(bar.close, state)
        
    gc.collect()
    
    # Snapshot at T=100000
    snapshot_end = tracemalloc.take_snapshot()
    tracemalloc.stop()
    
    # 3. Compare Snapshots
    stats = snapshot_end.compare_to(snapshot_start, 'lineno')
    
    # We only care about memory growth from OUR modules.
    # Python runtime might do tiny internal allocations, so we check total diff.
    total_diff_bytes = sum(stat.size_diff for stat in stats)
    
    # Allow a maximum of 500 KB drift over 100,000 operations
    # (In reality, O(1) SMAState drift should be exactly 0 bytes)
    max_drift_bytes = 500 * 1024 
    
    assert total_diff_bytes < max_drift_bytes, f"MEMORY LEAK DETECTED: {total_diff_bytes} bytes leaked."
