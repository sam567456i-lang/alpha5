import yaml

path = r"Docs\Governance\registry\rule_capability_registry.yaml"

with open(path, "r") as f:
    data = yaml.safe_load(f)

for cap_id, cap in data.get("mappings", {}).items():
    if "version" not in cap:
        cap["version"] = "1.0.0"
        cap["introduced_release"] = "0.8"
        cap["deprecated_by"] = None
        cap["replacement"] = None
        cap["compatible_with"] = {
            "EventSchema": {"min": "2.0.0"}
        }

with open(path, "w") as f:
    yaml.dump(data, f, sort_keys=False)
    
print("Appended versioning and compatibility to capabilities.")
