"""3-Tier Data Fixtures for AlphaGrid Testing.

Tiers:
1. Golden: 100% deterministic, perfect data (e.g., sine wave) for regression testing.
2. Synthetic: Statistically modeled data with controlled noise (e.g., GARCH) for integration testing.
3. Real: Sample historical data for pipeline/scientific validation.
"""

import os
import json
import hashlib
import unicodedata
import pandas as pd
import numpy as np
import pytest
from datetime import datetime, timezone, timedelta


def _format_float(val: float) -> str:
    return f"{val:.8f}"

def _generate_canonical_hash(df: pd.DataFrame) -> str:
    formatted_rows = []
    for _, row in df.iterrows():
        formatted_ts = row["timestamp"].strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        formatted_rows.append([
            formatted_ts,
            _format_float(row["open"]),
            _format_float(row["high"]),
            _format_float(row["low"]),
            _format_float(row["close"]),
            _format_float(row["volume"])
        ])
        
    canonical_json = json.dumps(formatted_rows, sort_keys=True, separators=(",", ":"))
    canonical_json = unicodedata.normalize("NFC", canonical_json)
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


@pytest.fixture(scope="session")
def fixture_dir():
    d = "tests/fixtures_data"
    os.makedirs(d, exist_ok=True)
    return d


@pytest.fixture(scope="session")
def golden_fixture(fixture_dir):
    """Tier 1: Golden Fixture (Deterministic sine wave)."""
    dates = [datetime(2025, 1, 1, tzinfo=timezone.utc) + timedelta(hours=i) for i in range(100)]
    t = np.linspace(0, 10 * np.pi, len(dates))
    base_price = 100.0
    prices = base_price + np.sin(t) * 10.0
    
    df = pd.DataFrame({
        "timestamp": dates,
        "open": prices,
        "high": prices + 0.5,
        "low": prices - 0.5,
        "close": prices,
        "volume": np.ones(len(dates)) * 500
    })
    
    path = os.path.join(fixture_dir, "golden.parquet")
    df.to_parquet(path, engine="pyarrow")
    snapshot_id = _generate_canonical_hash(df)
    
    return {"path": path, "snapshot_id": snapshot_id}


@pytest.fixture(scope="session")
def synthetic_fixture(fixture_dir):
    """Tier 2: Synthetic Fixture (Random walk with noise)."""
    dates = [datetime(2025, 1, 1, tzinfo=timezone.utc) + timedelta(hours=i) for i in range(500)]
    np.random.seed(123)
    returns = np.random.normal(0.0001, 0.005, len(dates))
    prices = 100.0 * np.exp(np.cumsum(returns))
    
    df = pd.DataFrame({
        "timestamp": dates,
        "open": prices,
        "high": prices * 1.002,
        "low": prices * 0.998,
        "close": prices,
        "volume": np.random.uniform(100, 1000, len(dates))
    })
    
    path = os.path.join(fixture_dir, "synthetic.parquet")
    df.to_parquet(path, engine="pyarrow")
    snapshot_id = _generate_canonical_hash(df)
    
    return {"path": path, "snapshot_id": snapshot_id}


@pytest.fixture(scope="session")
def real_fixture(fixture_dir):
    """Tier 3: Real Fixture (Sample OHLCV)."""
    # In a real setup, this would load a tiny slice of actual historical data.
    # For now, it mocks it with a different profile.
    dates = [datetime(2025, 1, 1, tzinfo=timezone.utc) + timedelta(days=i) for i in range(100)]
    np.random.seed(777)
    prices = 200.0 + np.cumsum(np.random.standard_t(df=3, size=len(dates)))
    
    df = pd.DataFrame({
        "timestamp": dates,
        "open": prices,
        "high": prices + 1.0,
        "low": prices - 1.0,
        "close": prices,
        "volume": np.random.lognormal(mean=10, sigma=1, size=len(dates))
    })
    
    path = os.path.join(fixture_dir, "real.parquet")
    df.to_parquet(path, engine="pyarrow")
    snapshot_id = _generate_canonical_hash(df)
    
    return {"path": path, "snapshot_id": snapshot_id}
