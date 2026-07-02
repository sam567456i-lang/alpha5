import os
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

def generate_synthetic(filename: str, n_bars: int = 5000, seed: int = 42, missing: bool = False, constant: bool = False):
    np.random.seed(seed)
    dates = [datetime(2025, 1, 1, tzinfo=timezone.utc) + timedelta(minutes=i*15) for i in range(n_bars)]
    
    if constant:
        prices = np.full(n_bars, 100.0)
    else:
        prices = 100.0 + np.cumsum(np.random.normal(0, 0.5, n_bars))
        
    open_p = prices
    high_p = prices + np.random.uniform(0.1, 1.0, n_bars)
    low_p = prices - np.random.uniform(0.1, 1.0, n_bars)
    close_p = open_p + np.random.normal(0, 0.3, n_bars)
    
    # Ensure High is max, Low is min
    high_p = np.maximum.reduce([open_p, high_p, close_p])
    low_p = np.minimum.reduce([open_p, low_p, close_p])
    
    vol = np.random.uniform(1000, 50000, n_bars)
    
    df = pd.DataFrame({
        "timestamp": dates,
        "open": open_p,
        "high": high_p,
        "low": low_p,
        "close": close_p,
        "volume": vol
    })
    
    if missing:
        # Introduce missing data (NaN) randomly
        missing_indices = np.random.choice(df.index, size=int(n_bars*0.05), replace=False)
        df.loc[missing_indices, "close"] = np.nan
        df.loc[missing_indices, "volume"] = np.nan

    df.to_csv(os.path.join(DATA_DIR, filename), index=False)
    print(f"Generated {filename}")

if __name__ == "__main__":
    generate_synthetic("synthetic.csv", n_bars=5000)
    generate_synthetic("historical_nifty.csv", n_bars=10000, seed=101)  # Proxy for historical
    generate_synthetic("historical_spy.csv", n_bars=10000, seed=202)    # Proxy for historical
    
    # Edge cases
    generate_synthetic("edge_empty.csv", n_bars=0)
    generate_synthetic("edge_constant.csv", n_bars=100, constant=True)
    generate_synthetic("edge_missing.csv", n_bars=1000, missing=True)
