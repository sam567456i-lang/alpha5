import yaml

path = r"Docs\Governance\registry\rule_evidence_registry.yaml"

with open(path, "r") as f:
    data = yaml.safe_load(f)

for k, v in data.get("evidence_types", {}).items():
    if "temporal_type" not in v:
        v["temporal_type"] = "State"

with open(path, "w") as f:
    yaml.dump(data, f, sort_keys=False)
    
print("Appended temporal_type to evidence_types.")
