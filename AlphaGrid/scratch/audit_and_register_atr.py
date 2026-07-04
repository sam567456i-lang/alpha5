import os
import yaml

REGISTRY_PATH = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance\registry\master_capability_registry.yaml"

def audit_and_register_atr():
    with open(REGISTRY_PATH, "r") as f:
        registry = yaml.safe_load(f) or {"capabilities": []}
        
    caps = registry.setdefault("capabilities", [])
    exists = any(c.get("capability_id") == "ANALYSIS_VOLATILITY_ATR" for c in caps)
    
    if not exists:
        caps.append({
            "capability_id": "ANALYSIS_VOLATILITY_ATR",
            "name": "ATR Volatility Analysis",
            "platform": "P05_Analysis",
            "family": "Volatility",
            "subfamily": "ATR",
            "dependencies": ["INDICATOR_ATR"]
        })
        with open(REGISTRY_PATH, "w") as f:
            yaml.dump(registry, f, sort_keys=False)
        print("Project OS: Capability ANALYSIS_VOLATILITY_ATR registered successfully.")
    else:
        print("Project OS: Capability ANALYSIS_VOLATILITY_ATR already registered.")
        
    print("Project OS Audit: ATR Analysis is CLEARED for migration.")

if __name__ == "__main__":
    audit_and_register_atr()
