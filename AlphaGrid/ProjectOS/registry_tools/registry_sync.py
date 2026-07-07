import os
import yaml

def sync_wave1_liquidity_capabilities(repo_root: str):
    cap_reg_path = os.path.join(repo_root, "Docs", "Governance", "registry", "capability_registry.yaml")
    
    with open(cap_reg_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {"entries": []}
        
    entries = data.get("entries", [])
    
    # Generic Time-based config
    time_based = {
        "detector": "TimeBasedLiquidityDetector",
        "tolerance": {"type": "absolute", "value": 0},
        "confidence_model": "static",
        "lineage_required": True,
        "latency_budget_ms": 10,
        "replay_supported": True,
        "deterministic": True,
        "supported_markets": ["CRYPTO", "FX", "EQUITY"],
        "supported_sessions": ["ALL"]
    }
    
    swing_based = time_based.copy()
    swing_based["detector"] = "SwingLiquidityDetector"
    
    equal_based = time_based.copy()
    equal_based["detector"] = "EqualLiquidityDetector"
    
    # Mapping
    liquidity_updates = {
        "CON-LIQ-PDH": {**time_based, "timeframe": "DAY", "lookback": 1, "detection_mode": "PREV_HIGH"},
        "CON-LIQ-PDL": {**time_based, "timeframe": "DAY", "lookback": 1, "detection_mode": "PREV_LOW"},
        "CON-LIQ-PWH": {**time_based, "timeframe": "WEEK", "lookback": 1, "detection_mode": "PREV_HIGH"},
        "CON-LIQ-PWL": {**time_based, "timeframe": "WEEK", "lookback": 1, "detection_mode": "PREV_LOW"},
        "CON-LIQ-PMH": {**time_based, "timeframe": "MONTH", "lookback": 1, "detection_mode": "PREV_HIGH"},
        "CON-LIQ-PML": {**time_based, "timeframe": "MONTH", "lookback": 1, "detection_mode": "PREV_LOW"},
        "CON-LIQ-SWINGHIGH": {**swing_based, "detection_mode": "SWING_HIGH"},
        "CON-LIQ-SWINGLOW": {**swing_based, "detection_mode": "SWING_LOW"},
        "CON-LIQ-EQH": {**equal_based, "detection_mode": "EQUAL_HIGHS"},
        "CON-LIQ-EQL": {**equal_based, "detection_mode": "EQUAL_LOWS"}
    }
    
    updated = 0
    for entry in entries:
        if entry["id"] in liquidity_updates:
            updates = liquidity_updates[entry["id"]]
            entry.setdefault("configuration", {}).update(updates)
            updated += 1
            
    with open(cap_reg_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, default_flow_style=False)
        
    print(f"Registry Sync Complete: Updated {updated} capabilities with generic detector configurations.")

if __name__ == "__main__":
    sync_wave1_liquidity_capabilities(r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid")
