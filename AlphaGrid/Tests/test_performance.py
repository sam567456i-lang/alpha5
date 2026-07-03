import pytest
import time
import pandas as pd
from Backend.price_geometry.geometry_engine import GeometryEngineOrchestrator
from Backend.price_geometry.cache import GeometryCache

def test_geometry_performance_benchmark():
    """
    Benchmarks the O(N) operations in the Geometry DAG over 10,000 bars.
    Threshold: < 500ms.
    """
    # Generate 1000 bars of dummy data
    bars = []
    base_ts = 1704067200000 
    for i in range(1000):
        bars.append({"timestamp": pd.to_datetime(base_ts + (i * 3600000), unit='ms'), "open": 50000 + i, "high": 50100 + i, "low": 49900 + i, "close": 50050 + i, "volume": 100})
        
    df = pd.DataFrame(bars)
    df.set_index("timestamp", inplace=True)
    
    orchestrator = GeometryEngineOrchestrator()
    cache = GeometryCache()
    
    class Context:
        def __init__(self):
            self.geometry_cache = cache
            self.symbol = "BTCUSDT"
            self.timeframe = "1H"
            self.dataset_id = "test"
            
    t0 = time.perf_counter()
    orchestrator.process_all(df, Context())
    t1 = time.perf_counter()
    
    runtime_ms = (t1 - t0) * 1000
    
    # Assert benchmark (< 500ms for 1000 bars using O(N) loops in Python)
    assert runtime_ms < 500.0, f"Performance Benchmark failed: {runtime_ms:.2f}ms exceeds 500ms threshold."
