import json
import os
from datetime import datetime, timedelta

def build_scenario(name, ticks, description):
    return {
        "scenario": name,
        "description": description,
        "ticks": ticks
    }

def save_scenario(output_dir, name, scenario_data):
    filepath = os.path.join(output_dir, f"{name}.json")
    with open(filepath, 'w') as f:
        json.dump(scenario_data, f, indent=4)

def generate_golden_datasets(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    now = datetime(2026, 7, 9, 10, 0, 0)
    
    # 1. Trending Market
    trend_ticks = []
    price = 100.0
    for i in range(10):
        trend_ticks.append({"timestamp": (now + timedelta(minutes=i)).isoformat(), "price": price})
        price += 1.0; price -= 0.25
    save_scenario(output_dir, "trend", build_scenario("TREND_UP", trend_ticks, "Smooth uptrend forming clear swing lows."))
    
    # 2. Ranging Market
    range_ticks = []
    for i in range(20):
        val = 100.0 if i % 2 == 0 else 105.0
        range_ticks.append({"timestamp": (now + timedelta(minutes=i)).isoformat(), "price": val})
    save_scenario(output_dir, "ranging", build_scenario("RANGE_FLAT", range_ticks, "Ping-pong between 100 and 105."))

    # 3. Gaps
    gap_ticks = [
        {"timestamp": now.isoformat(), "price": 100.0},
        {"timestamp": (now + timedelta(days=1)).isoformat(), "price": 150.0}
    ]
    save_scenario(output_dir, "gaps", build_scenario("GAP_UP", gap_ticks, "Overnight gap up."))

    # 4. Malformed
    malformed_ticks = [
        {"timestamp": now.isoformat(), "price": -50.0},
        {"timestamp": (now - timedelta(days=1)).isoformat(), "price": 100.0} # out of order
    ]
    save_scenario(output_dir, "malformed", build_scenario("MALFORMED", malformed_ticks, "Out of order and negative prices."))

    # 5. Crypto
    crypto_ticks = []
    for i in range(24):
        crypto_ticks.append({"timestamp": (now + timedelta(hours=i)).isoformat(), "price": 60000.0 + (i*10)})
    save_scenario(output_dir, "crypto", build_scenario("CRYPTO_247", crypto_ticks, "Continuous rolling prices."))

if __name__ == "__main__":
    generate_golden_datasets("Backend/tests/golden")
    print("Golden Reference Datasets Generated in golden/")
