import pandas as pd
import pytest
from datetime import datetime
from collections import namedtuple

from Backend.price_geometry.swing_engine import SwingEngine
from Backend.price_geometry.structure_engine import StructureEngine
from Backend.price_geometry.imbalance_engine import ImbalanceEngine

from Backend.price_geometry.objects import Pivot

class MockCache:
    def __init__(self, objects):
        self.objects = objects
    def get_by_type(self, obj_type, symbol):
        return [o for o in self.objects if type(o).__name__ == obj_type]

class MockContext:
    def __init__(self, pivots=None):
        self.dataset_id = "test_data"
        self.timeframe = "1D"
        self.symbol = "BTCUSDT"
        self.swings = []
        self.existing_imbalances = []
        self.geometry_cache = MockCache(pivots or [])

def test_imbalance_engine_fvg_known_values():
    """
    Test FVG detection with hardcoded, known values.
    """
    dates = pd.date_range("2026-01-01", periods=3)
    data = pd.DataFrame({
        "open": [100, 110, 120],
        "high": [105, 125, 130],
        "low": [95, 108, 115],
        "close": [100, 120, 125]
    }, index=dates)
    
    # Gap between Bar 1 High (105) and Bar 3 Low (115) -> Bullish FVG
    engine = ImbalanceEngine()
    context = MockContext()
    
    imbalances = engine.process(data, context)
    assert len(imbalances) == 1
    
    fvg = imbalances[0]
    assert fvg.imbalance_type == "FVG"
    assert fvg.is_bullish is True
    assert fvg.top_price == 115
    assert fvg.bottom_price == 105

def test_swing_engine_known_values():
    """
    Test Swing detection with a simple 3-bar fractal on known data.
    """
    dates = pd.date_range("2026-01-01", periods=5)
    data = pd.DataFrame({
        "open": [100, 100, 100, 100, 100],
        "high": [105, 110, 120, 110, 105], # High is at index 2 (120)
        "low": [90, 80, 70, 80, 90],       # Low is at index 2 (70)
        "close": [100, 100, 100, 100, 100]
    }, index=dates)
    
    # Static mode for predictable tests, strength = 2 (meaning 2 bars left, 2 bars right)
    # Total bars = 5 (indices 0, 1, 2, 3, 4). Bar 2 has 2 left, 2 right.
    engine = SwingEngine(mode="static", default_strength=2)
    pivots = [
        Pivot(id="P1", version="v1", dataset_id="test_data", symbol="BTCUSDT", timeframe="1D", timestamp=dates[0], price=105, is_high=True, left_bars=0, right_bars=0),
        Pivot(id="P2", version="v1", dataset_id="test_data", symbol="BTCUSDT", timeframe="1D", timestamp=dates[1], price=110, is_high=True, left_bars=1, right_bars=1),
        Pivot(id="P3", version="v1", dataset_id="test_data", symbol="BTCUSDT", timeframe="1D", timestamp=dates[2], price=120, is_high=True, left_bars=2, right_bars=2),
        Pivot(id="P4", version="v1", dataset_id="test_data", symbol="BTCUSDT", timeframe="1D", timestamp=dates[2], price=70, is_high=False, left_bars=2, right_bars=2),
    ]
    context = MockContext(pivots)
    
    swings = engine.process(data, context)
    assert len(swings) == 2
    
    highs = [s for s in swings if s.is_high]
    lows = [s for s in swings if not s.is_high]
    
    assert len(highs) == 1
    assert highs[0].price == 120
    
    assert len(lows) == 1
    assert lows[0].price == 70
