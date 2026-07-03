import time
import os
import psutil
import pandas as pd
import numpy as np
from datetime import datetime, timezone

from Backend.market_intelligence.normalization_engine import NormalizationEngine
from Backend.market_intelligence.mtf_alignment_engine import MTFAlignmentEngine

def generate_synthetic_data(num_bars: int) -> pd.DataFrame:
    idx = pd.date_range("2020-01-01", periods=num_bars, freq="5min", tz="UTC")
    df = pd.DataFrame({
        "open": np.random.uniform(100, 200, num_bars),
        "high": np.random.uniform(100, 200, num_bars),
        "low": np.random.uniform(100, 200, num_bars),
        "close": np.random.uniform(100, 200, num_bars),
        "volume": np.random.randint(1000, 50000, num_bars)
    }, index=idx)
    return df

def run_benchmarks():
    print("Starting Market Intelligence Performance Benchmarks...")
    process = psutil.Process(os.getpid())
    
    norm_engine = NormalizationEngine()
    mtf_engine = MTFAlignmentEngine()
    
    num_symbols = 1000
    bars_per_symbol = 1000 # ~2 weeks of 5m data
    
    # Pre-generate data to avoid timing the random generator
    raw_data = [generate_synthetic_data(bars_per_symbol) for _ in range(num_symbols)]
    higher_tf_data = [generate_synthetic_data(bars_per_symbol // 12) for _ in range(num_symbols)] # e.g. 1H
    
    start_mem = process.memory_info().rss / 1024 / 1024
    print(f"Base Memory: {start_mem:.2f} MB")
    
    start_time = time.perf_counter()
    latencies = []
    
    for i in range(num_symbols):
        t0 = time.perf_counter()
        
        # Pipeline: Normalize LTF -> Normalize HTF -> Align
        n_ltf = norm_engine.normalize(raw_data[i], symbol=f"SYM_{i}", timeframe="5m")
        n_htf = norm_engine.normalize(higher_tf_data[i], symbol=f"SYM_{i}", timeframe="1H")
        aligned = mtf_engine.align(n_ltf, n_htf)
        
        t1 = time.perf_counter()
        latencies.append(t1 - t0)
        
    end_time = time.perf_counter()
    end_mem = process.memory_info().rss / 1024 / 1024
    
    total_time = end_time - start_time
    avg_latency = np.mean(latencies) * 1000 # ms
    worst_case = np.max(latencies) * 1000 # ms
    throughput = num_symbols / total_time
    
    print("\n--- Benchmark Results ---")
    print(f"Symbols Processed: {num_symbols}")
    print(f"Total Time: {total_time:.4f} seconds")
    print(f"Throughput: {throughput:.2f} symbols/sec")
    print(f"Average Latency: {avg_latency:.2f} ms/symbol")
    print(f"Worst Case Latency: {worst_case:.2f} ms")
    print(f"Peak Memory: {end_mem:.2f} MB")
    
    # Write to a file for artifact generation
    with open("Docs/Phase_10B/benchmark_results.md", "w") as f:
        f.write("# Market Intelligence Performance Benchmark\n\n")
        f.write(f"- **Symbols Processed**: {num_symbols}\n")
        f.write(f"- **Total Time**: {total_time:.4f} seconds\n")
        f.write(f"- **Throughput**: {throughput:.2f} symbols/sec\n")
        f.write(f"- **Average Latency**: {avg_latency:.2f} ms/symbol\n")
        f.write(f"- **Worst Case Latency**: {worst_case:.2f} ms\n")
        f.write(f"- **Peak Memory Usage**: {end_mem:.2f} MB\n")

if __name__ == "__main__":
    # Ensure Docs directory exists
    os.makedirs("Docs/Phase_10B", exist_ok=True)
    run_benchmarks()
