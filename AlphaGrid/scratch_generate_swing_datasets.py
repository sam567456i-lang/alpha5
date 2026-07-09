import os
import json

base_dir = r"Backend\core\golden_dataset\structure"
dirs = ["positive", "negative", "edge_cases", "lifecycle"]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# 1. Positive: standard 5-bar swing high and low
# High at index 2 (120). Low at index 7 (80).
positive_data = [
    {"timestamp": "2026-01-01T00:00:00Z", "open": 100, "high": 110, "low": 90, "close": 105, "volume": 1000},
    {"timestamp": "2026-01-01T01:00:00Z", "open": 105, "high": 115, "low": 95, "close": 110, "volume": 1000},
    {"timestamp": "2026-01-01T02:00:00Z", "open": 110, "high": 120, "low": 100, "close": 115, "volume": 1000}, # SWING HIGH
    {"timestamp": "2026-01-01T03:00:00Z", "open": 115, "high": 110, "low": 95, "close": 100, "volume": 1000},
    {"timestamp": "2026-01-01T04:00:00Z", "open": 100, "high": 105, "low": 90, "close": 95, "volume": 1000},
    {"timestamp": "2026-01-01T05:00:00Z", "open": 95, "high": 100, "low": 85, "close": 90, "volume": 1000},
    {"timestamp": "2026-01-01T06:00:00Z", "open": 90, "high": 95, "low": 82, "close": 85, "volume": 1000},
    {"timestamp": "2026-01-01T07:00:00Z", "open": 85, "high": 90, "low": 80, "close": 88, "volume": 1000}, # SWING LOW
    {"timestamp": "2026-01-01T08:00:00Z", "open": 88, "high": 95, "low": 85, "close": 92, "volume": 1000},
    {"timestamp": "2026-01-01T09:00:00Z", "open": 92, "high": 100, "low": 90, "close": 98, "volume": 1000},
]

with open(os.path.join(base_dir, "positive", "swing.json"), "w") as f:
    json.dump(positive_data, f, indent=2)

# 2. Negative: monotonically increasing, no swings
negative_data = []
for i in range(10):
    negative_data.append({
        "timestamp": f"2026-01-01T{i:02d}:00:00Z",
        "open": 100 + i*5, "high": 110 + i*5, "low": 90 + i*5, "close": 105 + i*5, "volume": 1000
    })

with open(os.path.join(base_dir, "negative", "swing.json"), "w") as f:
    json.dump(negative_data, f, indent=2)

# 3. Edge Cases: Inside bars and equal highs
# High at index 2 (120), but index 3 is inside bar, index 4 is lower.
# Equal high at index 7 (130) and index 8 (130).
edge_cases_data = [
    {"timestamp": "2026-01-01T00:00:00Z", "open": 100, "high": 110, "low": 90, "close": 105, "volume": 1000},
    {"timestamp": "2026-01-01T01:00:00Z", "open": 105, "high": 115, "low": 95, "close": 110, "volume": 1000},
    {"timestamp": "2026-01-01T02:00:00Z", "open": 110, "high": 120, "low": 100, "close": 115, "volume": 1000}, # SWING HIGH
    {"timestamp": "2026-01-01T03:00:00Z", "open": 110, "high": 115, "low": 105, "close": 112, "volume": 1000}, # Inside bar
    {"timestamp": "2026-01-01T04:00:00Z", "open": 112, "high": 118, "low": 90, "close": 95, "volume": 1000},
    {"timestamp": "2026-01-01T05:00:00Z", "open": 95, "high": 110, "low": 85, "close": 105, "volume": 1000},
    {"timestamp": "2026-01-01T06:00:00Z", "open": 105, "high": 125, "low": 100, "close": 120, "volume": 1000},
    {"timestamp": "2026-01-01T07:00:00Z", "open": 120, "high": 130, "low": 115, "close": 125, "volume": 1000}, # Equal high 1
    {"timestamp": "2026-01-01T08:00:00Z", "open": 125, "high": 130, "low": 110, "close": 115, "volume": 1000}, # Equal high 2
    {"timestamp": "2026-01-01T09:00:00Z", "open": 115, "high": 125, "low": 100, "close": 110, "volume": 1000},
]

with open(os.path.join(base_dir, "edge_cases", "swing_inside_bars.json"), "w") as f:
    json.dump(edge_cases_data, f, indent=2)

# 4. Lifecycle: Nested swings (to test state maintenance)
lifecycle_data = positive_data # Reuse positive data for now as a lifecycle base
with open(os.path.join(base_dir, "lifecycle", "nested_swings.json"), "w") as f:
    json.dump(lifecycle_data, f, indent=2)

print("Generated all swing golden datasets.")
