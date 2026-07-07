import pytest
import pandas as pd
import numpy as np

# Mocking the math core for testing purposes since the real modules are in Backend
from Backend.math.public.sma import calculate_sma, SMAState, update_sma
from Backend.math.public.ema import calculate_ema, EMAState, update_ema
from Backend.core.dtos import OHLCV

def generate_test_data(size=1000):
    np.random.seed(42)
    prices = np.random.lognormal(mean=0.001, sigma=0.02, size=size)
    prices = np.cumprod(prices) * 100
    
    data = []
    for i, p in enumerate(prices):
        data.append(OHLCV(
            timestamp=i,
            open=p * 0.99,
            high=p * 1.02,
            low=p * 0.98,
            close=p,
            volume=1000,
            symbol="NIFTY"
        ))
    return data, pd.Series(prices)

def test_incremental_sma_matches_batch():
    """
    Gate 9: Incremental Validation
    Proves that O(1) SMA exactly matches O(N) batch SMA.
    """
    bars, prices = generate_test_data(100)
    period = 14
    
    # 1. Batch Calculation
    timestamps = np.arange(len(prices))
    batch_sma_result = calculate_sma(prices.values, timestamps, period)
    batch_sma = pd.Series(batch_sma_result.values)
    
    # 2. Incremental Calculation
    state = SMAState(period=period)
    
    incremental_results = []
    for bar in bars:
        val = update_sma(bar.close, state)
        incremental_results.append(val)
            
    incremental_series = pd.Series(incremental_results)
    
    # Assert they are effectively identical
    # We slice off the NaN prefix
    valid_batch = batch_sma.dropna()
    valid_incr = incremental_series[incremental_series.notna()]
    
    assert len(valid_batch) == len(valid_incr), "Length mismatch"
    
    # Check exact float equivalence up to 5 decimal places
    pd.testing.assert_series_equal(
        valid_batch.reset_index(drop=True), 
        valid_incr.reset_index(drop=True),
        check_names=False,
        rtol=1e-5
    )

def test_incremental_ema_matches_batch():
    """
    Gate 9: Incremental Validation
    Proves that O(1) EMA exactly matches O(N) batch EMA.
    """
    bars, prices = generate_test_data(100)
    period = 14
    
    # 1. Batch Calculation
    timestamps = np.arange(len(prices))
    batch_ema_result = calculate_ema(prices.values, timestamps, period)
    batch_ema = pd.Series(batch_ema_result.values)
    
    # 2. Incremental Calculation
    state = EMAState(period=period)
    
    incremental_results = []
    for bar in bars:
        val = update_ema(bar.close, state)
        incremental_results.append(val)
            
    incremental_series = pd.Series(incremental_results)
    
    # Assert they are identical
    valid_batch = batch_ema.dropna()
    valid_incr = incremental_series[incremental_series.notna()]
    
    assert len(valid_batch) == len(valid_incr), "Length mismatch"
    
    pd.testing.assert_series_equal(
        valid_batch.reset_index(drop=True), 
        valid_incr.reset_index(drop=True),
        check_names=False,
        rtol=1e-5
    )
