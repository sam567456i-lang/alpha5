import time
import numpy as np
from Backend.math.public.ema import calculate_ema

def run_benchmark():
    sizes = [100, 1000, 10000, 100000, 1000000]
    period = 14
    
    print("=== EMA Benchmark Baseline ===")
    print(f"{'Size':>10} | {'Runtime (ms)':>15} | {'Scaling':>10}")
    print("-" * 45)
    
    prev_time = None
    
    for size in sizes:
        # Generate synthetic data
        values = np.random.randn(size)
        timestamps = np.arange(size)
        
        # Warmup JIT if Numba was used (not currently, but good practice)
        _ = calculate_ema(values[:period+1], timestamps[:period+1], period)
        
        # Benchmark
        start = time.perf_counter()
        res = calculate_ema(values, timestamps, period)
        end = time.perf_counter()
        
        duration_ms = (end - start) * 1000.0
        
        scaling = "N/A"
        if prev_time is not None and prev_time > 0:
            scaling = f"{duration_ms / prev_time:.1f}x"
            
        print(f"{size:>10} | {duration_ms:>15.2f} | {scaling:>10}")
        prev_time = duration_ms

if __name__ == "__main__":
    run_benchmark()
