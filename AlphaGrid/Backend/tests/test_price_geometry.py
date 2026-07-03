import pytest
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

from Backend.price_geometry.cache import GeometryCache
from Backend.price_geometry.objects import Pivot, Swing, Trendline, Channel, Range
from Backend.price_geometry.pivot_engine import PivotEngine
from Backend.price_geometry.swing_engine import SwingEngine
from Backend.price_geometry.trendline_engine import TrendlineEngine
from Backend.price_geometry.channel_engine import ChannelEngine
from Backend.price_geometry.range_engine import RangeEngine
from Backend.price_geometry.geometry_engine import GeometryEngineOrchestrator

class MockContext:
    def __init__(self, cache, symbol="TEST", timeframe="1H"):
        self.geometry_cache = cache
        self.symbol = symbol
        self.timeframe = timeframe
        self.dataset_id = "test_data"

@pytest.fixture
def sample_data():
    """Generates simple sinusoidal price data to guarantee swings."""
    dates = [datetime(2023, 1, 1) + timedelta(hours=i) for i in range(100)]
    x = np.linspace(0, 4 * np.pi, 100)
    # Sine wave ranging from 90 to 110
    prices = 100 + 10 * np.sin(x)
    
    df = pd.DataFrame({
        'timestamp': dates,
        'open': prices,
        'high': prices + 1,
        'low': prices - 1,
        'close': prices,
        'volume': 1000
    })
    df.set_index('timestamp', inplace=True, drop=False)
    return df

def test_pivot_engine(sample_data):
    engine = PivotEngine(mode="static", default_strength=3)
    pivots = engine.process(sample_data, MockContext(GeometryCache()))
    
    assert len(pivots) > 0
    highs = [p for p in pivots if p.is_high]
    lows = [p for p in pivots if not p.is_high]
    assert len(highs) > 0
    assert len(lows) > 0

def test_orchestrator(sample_data):
    orchestrator = GeometryEngineOrchestrator()
    cache = GeometryCache()
    context = MockContext(cache)
    
    snapshot = orchestrator.process_all(sample_data, context)
    
    assert snapshot['total_pivots'] > 0
    assert snapshot['total_swings'] > 0
    # Trendlines depend on exact data alignment, might be 0 but shouldn't crash
    
    assert "symbol" in snapshot
    assert "new_objects_count" in snapshot

def test_cache():
    cache = GeometryCache()
    p = Pivot(
        id="test1", version="v1", dataset_id="ds1", symbol="BTC", timeframe="1H",
        timestamp=datetime.utcnow(), price=100.0,
        is_high=True, left_bars=3, right_bars=3
    )
    cache.add(p)
    assert cache.get("test1") == p
    assert len(cache.get_by_type("Pivot")) == 1
    assert len(cache.get_by_symbol("BTC")) == 1
