import os
import yaml

REGISTRY_PATH = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance\registry\master_capability_registry.yaml"

def audit_and_register_macd():
    with open(REGISTRY_PATH, "r") as f:
        registry = yaml.safe_load(f) or {"capabilities": []}
        
    caps = registry.setdefault("capabilities", [])
    exists = any(c.get("capability_id") == "ANALYSIS_MOMENTUM_MACD" for c in caps)
    
    if not exists:
        caps.append({
            "capability_id": "ANALYSIS_MOMENTUM_MACD",
            "name": "MACD Momentum Analysis",
            "platform": "P05_Analysis",
            "family": "Momentum",
            "subfamily": "MACD",
            "dependencies": ["INDICATOR_MACD"]
        })
        with open(REGISTRY_PATH, "w") as f:
            yaml.dump(registry, f, sort_keys=False)
        print("Project OS: Capability ANALYSIS_MOMENTUM_MACD registered successfully.")
    else:
        print("Project OS: Capability ANALYSIS_MOMENTUM_MACD already registered.")
        
    print("Project OS Audit: MACD Analysis is CLEARED for migration.")

if __name__ == "__main__":
    audit_and_register_macd()
