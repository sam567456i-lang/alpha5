import pytest
import numpy as np
import pandas as pd
import time
import psutil
import os
from Backend.reference.legacy.features.support_resistance import SupportResistanceFeatureGenerator
from Backend.reference.legacy.features.high_low_breakout import HighLowBreakoutFeatureGenerator


@pytest.fixture
def large_sample_data():
    np.random.seed(42)
    # 100,000 rows for stress testing
    periods = 100000
    dates = pd.date_range(start='2020-01-01', periods=periods, freq='min')
    df = pd.DataFrame({
        'open': np.random.uniform(100, 110, periods),
        'high': np.random.uniform(110, 120, periods),
        'low': np.random.uniform(90, 100, periods),
        'close': np.random.uniform(95, 115, periods),
        'volume': np.random.uniform(1000, 5000, periods),
    }, index=dates)
    df.attrs['symbol'] = 'TEST/USD'
    df.attrs['timeframe'] = '1m'
    return df


@pytest.fixture
def unstable_sample_data():
    np.random.seed(42)
    dates = pd.date_range(start='2026-01-01', periods=100, freq='D')
    df = pd.DataFrame({
        'open': np.random.uniform(100, 110, 100),
        'high': np.random.uniform(110, 120, 100),
        'low': np.random.uniform(90, 100, 100),
        'close': np.random.uniform(95, 115, 100),
        'volume': np.random.uniform(1000, 5000, 100),
    }, index=dates)
    
    # Inject NaN and Inf
    df.iloc[50, df.columns.get_loc('high')] = np.nan
    df.iloc[55, df.columns.get_loc('low')] = np.inf
    df.iloc[60, df.columns.get_loc('close')] = -np.inf
    
    df.attrs['symbol'] = 'TEST/USD'
    df.attrs['timeframe'] = '1d'
    return df


# --- Deterministic Replay ---

def test_explicit_deterministic_replay(large_sample_data):
    """Run #1 -> SHA256 -> Run #2 -> SHA256 -> Equal"""
    import hashlib
    
    gen1 = SupportResistanceFeatureGenerator(lookback=20)
    out1 = gen1.generate(large_sample_data, "trc-1", "cor-1")
    hash1 = hashlib.sha256(str(out1.values).encode()).hexdigest()
    
    gen2 = SupportResistanceFeatureGenerator(lookback=20)
    out2 = gen2.generate(large_sample_data, "trc-2", "cor-2")
    hash2 = hashlib.sha256(str(out2.values).encode()).hexdigest()
    
    assert hash1 == hash2, "Deterministic replay failed: Hashes do not match."


# --- Numerical Stability ---

def test_numerical_stability(unstable_sample_data):
    """Ensure features do not crash on NaN/Inf and handle it gracefully."""
    # Data preprocessing is expected to handle NaNs in production, but generators 
    # must survive dirty data without throwing unhandled native exceptions.
    gen = SupportResistanceFeatureGenerator(lookback=20)
    try:
        # We allow pandas to propagate NaNs, we just ensure it doesn't crash Python
        out = gen.generate(unstable_sample_data, "trc-1", "cor-1")
        assert 'resistance' in out.values
    except Exception as e:
        pytest.fail(f"Generator crashed on unstable data: {e}")


# --- Performance & Memory Budget ---

def test_performance_and_memory_budget(large_sample_data):
    """Ensure generator runs under runtime and memory budgets for 100k rows."""
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss
    
    start_time = time.time()
    
    gen = HighLowBreakoutFeatureGenerator(period=20)
    out = gen.generate(large_sample_data, "trc-1", "cor-1")
    
    runtime = time.time() - start_time
    mem_after = process.memory_info().rss
    
    mem_used_mb = (mem_after - mem_before) / (1024 * 1024)
    
    # Budgets: < 0.5 seconds for 100k rows, < 50MB overhead
    assert runtime < 0.5, f"Runtime budget exceeded: {runtime:.4f}s"
    # Note: Pandas memory management is tricky, we use a generous upper bound for testing
    assert mem_used_mb < 50.0, f"Memory budget exceeded: {mem_used_mb:.2f} MB"
