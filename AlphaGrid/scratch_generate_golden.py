import json
import os
import math

SCENARIOS = [
    "trending_bull", "trending_bear", "strong_range", "weak_range", "gap_open",
    "session_transition", "volatility_expansion", "volatility_compression",
    "liquidity_sweep", "structural_reversal"
]

BAR_COUNT = 1000

def generate_bars(scenario):
    bars = []
    base_price = 100.0
    for i in range(BAR_COUNT):
        if scenario == "trending_bull":
            base_price += 0.1
        elif scenario == "trending_bear":
            base_price -= 0.1
        elif "range" in scenario:
            base_price = 100.0 + (math.sin(i / 10.0) * (2.0 if "strong" in scenario else 0.5))
        elif scenario == "gap_open" and i == 500:
            base_price += 5.0
        elif scenario == "volatility_expansion":
            base_price += math.sin(i) * (i / 100.0)
        elif scenario == "volatility_compression":
            base_price += math.sin(i) * ((BAR_COUNT - i) / 100.0)
        elif scenario == "liquidity_sweep" and i == 500:
            bars[-1]["low"] -= 5.0
            bars[-1]["close"] += 2.0
            continue
        elif scenario == "structural_reversal":
            if i < 500:
                base_price -= 0.1
            else:
                base_price += 0.15
        
        # simple OHLC
        high = base_price + 0.5
        low = base_price - 0.5
        close = base_price
        
        bars.append({
            "timestamp": 1600000000000 + (i * 60000),
            "open": base_price,
            "high": high,
            "low": low,
            "close": close,
            "volume": 1000
        })
    return bars

def main():
    target_dir = r"Docs\Certification\tier0_golden_dataset"
    os.makedirs(target_dir, exist_ok=True)
    
    for scenario in SCENARIOS:
        bars = generate_bars(scenario)
        with open(os.path.join(target_dir, f"{scenario}.json"), "w") as f:
            json.dump({"scenario": scenario, "bars": bars}, f, indent=2)
            
    print(f"Generated {len(SCENARIOS)} golden datasets.")

if __name__ == "__main__":
    main()
