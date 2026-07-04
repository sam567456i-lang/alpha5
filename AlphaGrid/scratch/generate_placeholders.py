import yaml

REGISTRY_PATH = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance\registry\master_capability_registry.yaml"

families = [
    "Price Action", "Candlestick", "Chart Patterns", "Market Structure",
    "Support Resistance Structure", "Multi Timeframe", "Smart Money",
    "Liquidity", "Order Flow", "Market Profile", "Relative Strength",
    "Breadth", "Correlation", "Risk", "Statistical", "Quantitative",
    "Fundamental", "Macro", "Intermarket", "Seasonality", "Sentiment",
    "Behavioral", "Options", "On-chain", "Machine Learning", "AI Analysis",
    "External Repository Analysis"
]

with open(REGISTRY_PATH, "r") as f:
    registry = yaml.safe_load(f) or {"capabilities": []}
caps = registry.setdefault("capabilities", [])

for fam in families:
    cid_friendly = fam.upper().replace(" ", "_").replace("-", "_")
    cid = f"ANALYSIS_PLACEHOLDER_{cid_friendly}"
    
    exists = any(c.get("capability_id") == cid for c in caps)
    if not exists:
        caps.append({
            "capability_id": cid,
            "name": f"{fam} Analysis Placeholder",
            "platform": "P05_Analysis",
            "family": fam,
            "subfamily": "TBD",
            "dependencies": [],
            "status": "planned"
        })
        print(f"Registered placeholder for {fam}")

with open(REGISTRY_PATH, "w") as f:
    yaml.dump(registry, f, sort_keys=False)

print("All Phase 5D families registered as placeholders.")
