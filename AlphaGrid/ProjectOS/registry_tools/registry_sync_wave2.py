import yaml
import os
from datetime import datetime, timezone

REGISTRY_PATH = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\master_capability_registry.yaml"
BEHAVIOR_REGISTRY_PATH = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Docs\Governance\registry\behavior_registry.yaml"

WAVE_2_CAPABILITIES = [
    # Structure Objects
    {"id": "str.obj.swing", "name": "Swing Structure", "type": "StructureObject"},
    {"id": "str.obj.internal", "name": "Internal Structure", "type": "StructureObject"},
    {"id": "str.obj.external", "name": "External Structure", "type": "StructureObject"},
    {"id": "str.obj.fractal", "name": "Fractal Structure", "type": "StructureObject"},
    # Structure Events
    {"id": "str.eve.bos", "name": "Break of Structure (BOS)", "type": "StructureEvent"},
    {"id": "str.eve.ibos", "name": "Internal BOS", "type": "StructureEvent"},
    {"id": "str.eve.ebos", "name": "External BOS", "type": "StructureEvent"},
    {"id": "str.eve.mss", "name": "Market Structure Shift (MSS)", "type": "StructureEvent"},
    {"id": "str.eve.choch", "name": "Change of Character (CHOCH)", "type": "StructureEvent"},
    # Structure Context
    {"id": "str.con.htfbias", "name": "Higher Timeframe Bias", "type": "StructureContext"},
    {"id": "str.con.itrend", "name": "Internal Trend", "type": "StructureContext"},
    {"id": "str.con.etrend", "name": "External Trend", "type": "StructureContext"}
]

WAVE_2_BEHAVIORS = [
    {
        "id": "BEH-STR-001",
        "trigger": {"concept": "str.eve.bos"},
        "supports": ["str.con.continuation"],
        "weakens": ["str.con.reversal"],
        "invalidates": [],
        "requires": ["str.obj.swing"],
        "emits": ["StructureContinuationEvent"],
        "confidence_modifier": 0.2
    },
    {
        "id": "BEH-STR-002",
        "trigger": {"concept": "str.eve.choch"},
        "supports": ["str.con.reversal"],
        "weakens": [],
        "invalidates": ["str.con.prevtrend"],
        "requires": ["str.obj.swing"],
        "emits": ["StructureReversalEvent"],
        "confidence_modifier": 0.3
    },
    {
        "id": "BEH-STR-003",
        "trigger": {"concept": "str.eve.mss"},
        "supports": ["str.eve.choch"],
        "weakens": [],
        "invalidates": [],
        "requires": ["str.obj.swing"],
        "emits": ["StructureShiftEvent"],
        "confidence_modifier": 0.15
    }
]

def update_capability_registry():
    with open(REGISTRY_PATH, "r") as f:
        data = yaml.safe_load(f)

    existing_ids = {c["id"] for c in data.get("capabilities", [])}
    
    for cap in WAVE_2_CAPABILITIES:
        if cap["id"] not in existing_ids:
            new_cap = {
                "id": cap["id"],
                "name": cap["name"],
                "display_name": cap["name"],
                "description": f"Generic Structure definition for {cap['name']}",
                "family": "Structure",
                "lifecycle_state": "Implemented",
                "version": "1.0",
                "config": {
                    "detector": "GenericStructureDetector",
                    "detection_type": cap["type"].upper().replace("STRUCTURE", ""),
                },
                "consumes": ["ANA_PRICE_ACTION_SWING"],
                "produces": [f"ANA_MARKET_STRUCTURE_{cap['type'].upper()}"]
            }
            data["capabilities"].append(new_cap)

    data["generated_at"] = datetime.now(timezone.utc).isoformat()
    
    with open(REGISTRY_PATH, "w") as f:
        yaml.dump(data, f, sort_keys=False)
    print(f"Added {len(WAVE_2_CAPABILITIES)} capabilities to master registry.")

def update_behavior_registry():
    with open(BEHAVIOR_REGISTRY_PATH, "r") as f:
        data = yaml.safe_load(f)

    existing_ids = {b["id"] for b in data.get("entries", [])}
    
    for beh in WAVE_2_BEHAVIORS:
        if beh["id"] not in existing_ids:
            data["entries"].append(beh)

    with open(BEHAVIOR_REGISTRY_PATH, "w") as f:
        yaml.dump(data, f, sort_keys=False)
    print(f"Added {len(WAVE_2_BEHAVIORS)} behaviors to behavior registry.")

if __name__ == "__main__":
    update_capability_registry()
    update_behavior_registry()
