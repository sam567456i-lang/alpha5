"""
Generates the immutable golden dataset for E2E verification.
Run ONCE to create the fixture. Never regenerate without --force.

Output: Backend/tests/golden_data/BTCUSDT_1H_GOLDEN.json
"""
import json
import math
import os
import sys
from datetime import datetime, timezone, timedelta


def generate_golden_dataset(force: bool = False):
    """
    Generates 1000 hourly OHLCV bars with deterministic sinusoidal price action.
    Uses pure math (no random state) to guarantee identical output on any platform.
    
    Guard: refuses to overwrite an existing golden file without --force.
    """
    out_dir = os.path.join(os.path.dirname(__file__), "golden_data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "BTCUSDT_1H_GOLDEN.json")

    if os.path.exists(out_path) and not force:
        print(f"ERROR: Golden dataset already exists at {out_path}")
        print("Refusing to overwrite. Use --force to regenerate intentionally.")
        print("WARNING: Regenerating will invalidate the locked trade_sequence_hash baseline.")
        sys.exit(1)

    data = []
    base_ts = datetime(2024, 1, 1, tzinfo=timezone.utc)

    for i in range(1000):
        ts = base_ts + timedelta(hours=i)
        # Deterministic price curve: sinusoidal with trend.
        # No random seed involved — pure math guarantees cross-platform identity.
        base_price = 40000.0 + (i * 0.5) + math.sin(i * 0.1) * 1000.0
        high_offset = abs(math.sin(i * 0.3)) * 150.0 + 50.0
        low_offset = abs(math.cos(i * 0.3)) * 150.0 + 50.0
        close_shift = math.sin((i + 1) * 0.1) * 500.0

        data.append({
            "timestamp": ts.isoformat(),
            "symbol": "BTCUSDT",
            "open": round(base_price, 2),
            "high": round(base_price + high_offset, 2),
            "low": round(base_price - low_offset, 2),
            "close": round(base_price + close_shift, 2),
            "volume": round(100.0 + math.sin(i * 0.05) * 50.0, 2)
        })

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"))

    print(f"Golden dataset written: {out_path} ({len(data)} bars)")
    return out_path


if __name__ == "__main__":
    force = "--force" in sys.argv
    generate_golden_dataset(force=force)
