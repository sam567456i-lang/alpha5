import yaml
import os

repo_root = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
registry_path = os.path.join(repo_root, "master_capability_registry.yaml")

with open(registry_path, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

for cap in data["capabilities"]:
    if cap["id"] == "cap_meth_trend_core":
        cap["description"] = "Capability-driven Trend methodology evaluating abstract states"
        cap["required_features"] = ["TrendStructure", "TrendDirection", "TrendPersistence", "MarketRegime", "Momentum", "Volatility", "PricePosition"]
        # Add the advertised compatibilities to the registry metadata
        cap["compatible_with"] = ["Momentum", "Breakout", "ICT", "Wyckoff"]
        break

with open(registry_path, "w", encoding="utf-8") as f:
    yaml.dump(data, f, sort_keys=False, indent=2)

print("Updated cap_meth_trend_core in master_capability_registry.yaml")
