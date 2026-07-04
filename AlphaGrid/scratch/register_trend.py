import os
import yaml

REGISTRY_PATH = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance\registry\master_capability_registry.yaml"

def register_trend():
    with open(REGISTRY_PATH, "r") as f:
        registry = yaml.safe_load(f) or {"capabilities": []}
        
    caps = registry.setdefault("capabilities", [])
    
    new_caps = [
        {
            "capability_id": "ANALYSIS_TREND_SMA",
            "name": "SMA Trend Analysis",
            "platform": "P05_Analysis",
            "family": "Trend",
            "subfamily": "SMA",
            "dependencies": ["INDICATOR_SMA"]
        },
        {
            "capability_id": "ANALYSIS_TREND_WMA",
            "name": "WMA Trend Analysis",
            "platform": "P05_Analysis",
            "family": "Trend",
            "subfamily": "WMA",
            "dependencies": ["INDICATOR_WMA"]
        },
        {
            "capability_id": "ANALYSIS_TREND_MA_CROSS",
            "name": "MA Cross Trend Analysis",
            "platform": "P05_Analysis",
            "family": "Trend",
            "subfamily": "MACross",
            "dependencies": ["INDICATOR_SMA"]
        }
    ]
    
    existing_ids = {c.get("capability_id") for c in caps}
    for nc in new_caps:
        if nc["capability_id"] not in existing_ids:
            caps.append(nc)
            
    with open(REGISTRY_PATH, "w") as f:
        yaml.dump(registry, f, sort_keys=False)
        
    print("Registered remaining Group 1 Trend capabilities.")

if __name__ == "__main__":
    register_trend()
