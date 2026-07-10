import csv
import math
import random
import os

def generate_synthetic_data(output_path: str = "ENG-SYN-0001.csv", num_bars: int = 10000, seed: int = 42):
    """
    Generates a highly deterministic synthetic OHLCV dataset.
    Uses a seeded random generator and trigonometric functions to simulate price action
    without relying on external stochastic processes.
    """
    random.seed(seed)
    
    # Starting price
    price = 50000.0
    
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "open", "high", "low", "close", "volume"])
        
        base_time = 1704067200000 # Jan 1, 2024
        interval = 3600000 # 1 hour
        
        for i in range(num_bars):
            # Deterministic pseudo-volatility
            vol = math.sin(i / 100.0) * 50 + random.uniform(-10, 10)
            
            o = price
            h = price + abs(vol) + random.uniform(1, 10)
            l = price - abs(vol) - random.uniform(1, 10)
            c = price + vol
            
            # Ensure high is highest and low is lowest
            h = max(o, c, h)
            l = min(o, c, l)
            
            volume = random.uniform(10, 1000)
            
            writer.writerow([base_time + (i * interval), round(o, 2), round(h, 2), round(l, 2), round(c, 2), round(volume, 2)])
            
            price = c
            
    return os.path.abspath(output_path)

if __name__ == "__main__":
    generate_synthetic_data()
    print("Generated ENG-SYN-0001.csv")
