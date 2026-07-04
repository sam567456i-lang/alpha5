import os
import json
import numpy as np
import pandas as pd

def generate_datasets():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    datasets_dir = os.path.join(base_dir, "Datasets")
    
    # 1. Generate Synthetic Math Identities
    # Prove that Rolling Mean == Rolling Sum / Window
    # Prove that Var == E[x^2] - (E[x])^2
    np.random.seed(42)
    synthetic_prices = np.random.randn(1000) * 10 + 100
    synthetic_timestamps = np.arange(1000)
    
    identities_path = os.path.join(datasets_dir, "synthetic", "math_identities.json")
    with open(identities_path, "w") as f:
        json.dump({
            "prices": synthetic_prices.tolist(),
            "timestamps": synthetic_timestamps.tolist(),
            "description": "Base random array for identity proofs."
        }, f)
        
    # 2. Generate Golden Reference data (e.g. EMA using Pandas)
    golden_df = pd.DataFrame({
        "close": synthetic_prices,
        "volume": np.random.randint(100, 1000, 1000)
    })
    
    # MACD standard inputs
    golden_df['ema_12'] = golden_df['close'].ewm(span=12, adjust=False).mean()
    golden_df['ema_26'] = golden_df['close'].ewm(span=26, adjust=False).mean()
    
    # Primitives
    golden_df['ema_14'] = golden_df['close'].ewm(span=14, adjust=False).mean()
    golden_df['sma_14'] = golden_df['close'].rolling(window=14).mean()
    golden_df['wma_14'] = golden_df['close'].rolling(window=14).apply(
        lambda x: np.sum(x * np.arange(1, 15)) / np.sum(np.arange(1, 15)), raw=True
    )
    golden_df['var_14'] = golden_df['close'].rolling(window=14).var(ddof=1)
    golden_df['std_14'] = golden_df['close'].rolling(window=14).std(ddof=1)
    
    # New Wave 0 Primitives
    golden_df['roll_max_14'] = golden_df['close'].rolling(window=14).max()
    golden_df['roll_min_14'] = golden_df['close'].rolling(window=14).min()
    golden_df['diff_14'] = golden_df['close'].diff(periods=14)
    golden_df['shift_14'] = golden_df['close'].shift(periods=14)
    golden_df['cov_14'] = golden_df['close'].rolling(window=14).cov(golden_df['volume'], ddof=1)
    golden_df['corr_14'] = golden_df['close'].rolling(window=14).corr(golden_df['volume'])
    
    # Ensure numerical stability in edge cases
    golden_df = golden_df.fillna(np.nan)
    
    golden_path = os.path.join(datasets_dir, "golden", "reference.parquet")
    golden_df.to_parquet(golden_path)
    
    # 3. Generate Stress / Edge Cases
    edge_cases = {
        "nan_islands": [1.0, 2.0, np.nan, np.nan, 3.0, 4.0, np.nan, 5.0, 6.0, 7.0],
        "alternating_inf": [1.0, np.inf, 2.0, -np.inf, 3.0, np.inf, 4.0],
        "step_function": [1.0] * 50 + [100.0] * 50,
        "single_spike": [1.0] * 49 + [1000.0] + [1.0] * 50,
        "zero_variance": [5.0] * 100,
        "denormalized": [1e-300, 2e-300, 3e-300, 4e-300],
        "random_walk": np.cumsum(np.random.randn(100)).tolist()
    }
    
    # Clean up NaNs and Infs for JSON compatibility
    clean_edge_cases = {}
    for k, v in edge_cases.items():
        clean_v = []
        for val in v:
            if np.isnan(val):
                clean_v.append("NaN")
            elif val == np.inf:
                clean_v.append("Inf")
            elif val == -np.inf:
                clean_v.append("-Inf")
            else:
                clean_v.append(float(val))
        clean_edge_cases[k] = clean_v
        
    edge_cases_path = os.path.join(datasets_dir, "stress", "edge_cases.json")
    with open(edge_cases_path, "w") as f:
        json.dump(clean_edge_cases, f, indent=2)
        
    # 4. Generate Dataset Manifest
    import hashlib
    with open(golden_path, "rb") as f:
        golden_checksum = hashlib.sha256(f.read()).hexdigest()
        
    manifest = {
        "dataset_id": "DS-2026-MATH-001",
        "version": "1.0.0",
        "generator": "generate_golden_reference.py",
        "seed": 42,
        "reference_implementation": "pandas_ewm_1.5.0",
        "checksums": {
            "golden_reference.parquet": golden_checksum
        }
    }
    
    manifest_path = os.path.join(datasets_dir, "dataset_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

if __name__ == "__main__":
    generate_datasets()
    print("Datasets generated successfully.")
