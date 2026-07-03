import cProfile
import pstats
import pandas as pd
import numpy as np
from datetime import datetime

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

def profile_stress():
    periods = 10000 # reduced from 100k to 10k to finish quickly if O(N^2)
    dates = pd.date_range("2026-01-01", periods=periods, freq="min")
    data = pd.DataFrame({
        "open": np.random.uniform(100, 200, periods),
        "high": np.random.uniform(105, 205, periods),
        "low": np.random.uniform(95, 195, periods),
        "close": np.random.uniform(100, 200, periods)
    }, index=dates)
    
    pivots = [
        Pivot(id=f"P{i}", version="v1", dataset_id="stress", symbol="BTCUSDT", timeframe="1m", timestamp=dates[i], price=150.0, is_high=True, left_bars=5, right_bars=5)
        for i in range(periods)
    ]
    context = MockContext(pivots)
    
    swing_engine = SwingEngine(mode="adaptive", default_strength=3)
    swings = swing_engine.process(data, context)
    
    context.swings = swings
    struct_engine = StructureEngine()
    struct_engine.process(data, context)

if __name__ == "__main__":
    cProfile.run("profile_stress()", "stress.prof")
    p = pstats.Stats("stress.prof")
    p.strip_dirs().sort_stats("time").print_stats(20)
