import pickle
import pandas as pd
import numpy as np
import time

from Backend.price_geometry.swing_engine import SwingEngine
from Backend.price_geometry.structure_engine import StructureEngine
from Backend.price_geometry.objects import Pivot

class MockCache:
    def __init__(self, objects):
        self.objects = objects
    def get_by_type(self, obj_type, symbol):
        return [o for o in self.objects if type(o).__name__ == obj_type]

class MockContext:
    def __init__(self, pivots=None):
        self.dataset_id = "stress_test_data"
        self.timeframe = "1m"
        self.symbol = "BTCUSDT"
        self.swings = []
        self.geometry_cache = MockCache(pivots or [])

def generate_reference():
    # Use a small set (5000 bars) for quick generation of exactly identical outputs
    periods = 5000
    dates = pd.date_range("2026-01-01", periods=periods, freq="min")
    np.random.seed(42) # Deterministic data
    data = pd.DataFrame({
        "open": np.random.uniform(100, 200, periods),
        "high": np.random.uniform(105, 205, periods),
        "low": np.random.uniform(95, 195, periods),
        "close": np.random.uniform(100, 200, periods)
    }, index=dates)
    
    pivots = []
    for i in range(periods):
        is_high = (i % 2 == 0)
        price = 150.0 + (np.sin(i / 10.0) * 10) + np.random.uniform(-1, 1)
        pivots.append(Pivot(id=f"P{i}", version="v1", dataset_id="stress", symbol="BTCUSDT", timeframe="1m", timestamp=dates[i], price=price, is_high=is_high, left_bars=5, right_bars=5))
    
    context = MockContext(pivots)
    
    swing_engine = SwingEngine(mode="adaptive", default_strength=3)
    swings = swing_engine.process(data, context)
    
    context.swings = swings
    struct_engine = StructureEngine()
    
    start = time.perf_counter()
    structures = struct_engine.process(data, context)
    end = time.perf_counter()
    print(f"Generated {len(structures)} structures in {end - start:.2f}s")
    
    # Save the output and data to disk
    with open('scratch/semantic_reference.pkl', 'wb') as f:
        pickle.dump({
            "data": data,
            "swings": swings,
            "structures": structures
        }, f)

if __name__ == "__main__":
    generate_reference()
