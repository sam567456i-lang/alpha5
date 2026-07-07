import pytest
import numpy as np
import concurrent.futures

from Backend.math.public.sma import SMAState, update_sma
from Backend.core.dtos import OHLCV

def generate_feed(symbol: str, size: int = 100):
    """Generates a deterministic feed unique to a symbol"""
    # Use a deterministic integer from the symbol name instead of hash()
    seed = int(symbol.split("_")[1])
    rng = np.random.default_rng(seed)
    prices = rng.lognormal(mean=0.001, sigma=0.02, size=size)
    prices = np.cumprod(prices) * 100
    
    feed = []
    for i, p in enumerate(prices):
        feed.append(OHLCV(timestamp=i, open=p, high=p, low=p, close=p, volume=100, symbol=symbol))
    return feed

def process_symbol(symbol: str):
    """Processes a single symbol feed incrementally and returns the final state"""
    feed = generate_feed(symbol, size=500)
    state = SMAState(period=20)
    
    for bar in feed:
        update_sma(bar.close, state)
        
    return symbol, float(state.window_sum)

def test_concurrency_gate_7():
    """
    Gate 7: Concurrency Testing
    Proves that running deterministic indicators over N symbols in a single thread 
    yields the EXACT same final states as distributing them across an 8-Worker Pool.
    """
    symbols = [f"SYMBOL_{i}" for i in range(1, 17)] # 16 symbols
    
    # 1. Single Threaded Execution
    single_thread_results = {}
    for sym in symbols:
        s, final_sum = process_symbol(sym)
        single_thread_results[s] = final_sum
        
    # 2. Concurrent 8-Worker Execution
    concurrent_results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(process_symbol, sym): sym for sym in symbols}
        for future in concurrent.futures.as_completed(futures):
            s, final_sum = future.result()
            concurrent_results[s] = final_sum
            
    # 3. Validation
    for sym in symbols:
        seq_res = single_thread_results[sym]
        con_res = concurrent_results[sym]
        # Must be exactly identical
        assert seq_res == con_res, f"Concurrency failure on {sym}: {seq_res} != {con_res}"
