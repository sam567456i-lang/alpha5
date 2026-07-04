import yaml
import os

GOVERNANCE_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance\registry"
MASTER_FILE = os.path.join(GOVERNANCE_DIR, "master_capability_registry.yaml")

with open(MASTER_FILE, "r") as f:
    master = yaml.safe_load(f)

capabilities = master.get("capabilities", [])

registries = {
    "indicator_registry.yaml": {"indicators": []},
    "analysis_registry.yaml": {"analyses": []},
    "concept_registry.yaml": {"concepts": []},
    "methodology_registry.yaml": {"methodologies": []},
    "signal_registry.yaml": {"signals": []},
    "strategy_registry.yaml": {"strategies": []},
    "dashboard_registry.yaml": {"widgets": []},
    "ai_registry.yaml": {"agents": []},
    "validator_registry.yaml": {"validators": []}
}

for cap in capabilities:
    platform = cap.get("platform", "")
    if "Analysis" in platform:
        registries["analysis_registry.yaml"]["analyses"].append(cap)
    elif "Strategies" in platform:
        registries["strategy_registry.yaml"]["strategies"].append(cap)
    elif "Indicators" in platform:
        registries["indicator_registry.yaml"]["indicators"].append(cap)
    else:
        # Fallback to analysis
        registries["analysis_registry.yaml"]["analyses"].append(cap)

for filename, content in registries.items():
    filepath = os.path.join(GOVERNANCE_DIR, filename)
    with open(filepath, "w") as f:
        yaml.dump(content, f, sort_keys=False)
        print(f"Created {filename} with {len(list(content.values())[0])} records.")

# Delete old master
os.remove(MASTER_FILE)
print("Deleted master_capability_registry.yaml")
