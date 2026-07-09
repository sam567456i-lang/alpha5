import yaml

path = r"Docs\Governance\registry\rule_evidence_registry.yaml"

with open(path, "r") as f:
    data = yaml.safe_load(f)

for k, v in data.get("evidence_types", {}).items():
    if "interpretation_level" not in v:
        v["interpretation_level"] = "objective"

with open(path, "w") as f:
    yaml.dump(data, f, sort_keys=False)
    
print("Appended interpretation_level to evidence_types.")
