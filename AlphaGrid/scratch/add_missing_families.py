import yaml
import os

REGISTRY_PATH = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance\registry\analysis_registry.yaml"

with open(REGISTRY_PATH, "r") as f:
    data = yaml.safe_load(f)

analyses = data.get("analyses", [])

new_fams = [
    ("ANALYSIS_EXECUTION", "Execution Analysis", "Execution"),
    ("ANALYSIS_DATA_QUALITY", "Data Quality Analysis", "Data Quality"),
    ("ANALYSIS_MARKET_REGIME", "Market Regime Analysis", "Market Regime"),
    ("ANALYSIS_CROSS_ASSET", "Cross Asset Analysis", "Cross Asset"),
    ("ANALYSIS_PORTFOLIO_CONTEXT", "Portfolio Context", "Portfolio Context")
]

for cid, name, category in new_fams:
    if not any(c.get("capability_id") == cid for c in analyses):
        analyses.append({
            "capability_id": cid,
            "name": name,
            "platform": "P06_Analysis",
            "category": category,
            "family": category,
            "status": "planned"
        })
        print(f"Added {cid}")

with open(REGISTRY_PATH, "w") as f:
    yaml.dump(data, f, sort_keys=False)

print("Finished adding new families.")
