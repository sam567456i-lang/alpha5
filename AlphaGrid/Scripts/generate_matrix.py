import os, yaml, csv
GOV_REG = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance\registry\master_capability_registry.yaml"
OUT_CSV = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Docs\Roadmaps\Master_Capability_Matrix.csv"

with open(GOV_REG, 'r') as f:
    data = yaml.safe_load(f)

capabilities = data.get('capabilities', [])
if capabilities:
    headers = list(capabilities[0].keys())
    with open(OUT_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(capabilities)
print("Generated Master_Capability_Matrix.csv")
