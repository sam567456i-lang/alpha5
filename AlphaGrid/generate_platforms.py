import os

base_dir = "C:/Users/praka/Documents/Codex/2026-06-30/alphagrid-infinity-x-5-0-master/AlphaGrid/Docs/Platforms"
os.makedirs(base_dir, exist_ok=True)

platforms = {
    "Platform10": {
        "title": "Platform 10: Objective Evidence",
        "purpose": "Converts raw market data into canonical, objective evidence graphs. Contains zero subjectivity.",
        "allowed": ["New objective evidence (Indicators, Geometry)", "Performance optimization", "Bug fixes"],
        "forbidden": ["Methodology Interpretation", "Decisions", "Trading logic", "Subjective thresholds"]
    },
    "Platform11": {
        "title": "Platform 11: Methodology Interpretation",
        "purpose": "Applies methodology profiles (ICT, SMC, Wyckoff) to objective evidence, outputting subjective interpretations.",
        "allowed": ["New Profiles (YAML)", "New Policies", "New Projection Rules", "New Methodology Packages"],
        "forbidden": ["Custom Indicators", "Evidence Mutation", "Decision Making", "Execution Directives"]
    },
    "Platform12": {
        "title": "Platform 12: Decision Support",
        "purpose": "Consumes interpretation graphs and produces strategic execution plans, managing conflict and risk.",
        "allowed": ["Decision Feature Extraction", "Methodology Consensus", "Confidence Calibration", "Decision Graph Nodes"],
        "forbidden": ["Direct Market Data access", "Live Order Routing", "Broker Implementations"]
    },
    "Platform13": {
        "title": "Platform 13: Execution Intelligence",
        "purpose": "Converts strategic execution plans into tactical order sequences and interfaces with the broker.",
        "allowed": ["Order Sequencing", "Scaling Logic", "Trailing Stops", "Broker Adapters", "Slippage Estimation"],
        "forbidden": ["Strategic Decision Making", "Methodology Interpretation", "Learning/Calibration"]
    },
    "Platform14": {
        "title": "Platform 14: Learning & Analytics",
        "purpose": "Consumes the entire history of evidence, decisions, and execution to run attribution and statistical learning.",
        "allowed": ["Replay Analytics", "Attribution", "Drift Detection", "ML/RL Optimization", "Calibration"],
        "forbidden": ["Mutating Historical Evidence", "Direct live execution routing"]
    },
    "Platform15": {
        "title": "Platform 15: External Interfaces",
        "purpose": "The universal consumer layer. Exposes the internal intelligence to the outside world.",
        "allowed": ["Dashboards", "REST APIs", "CLI", "Webhooks", "SDKs", "Mobile Apps"],
        "forbidden": ["Business Logic", "State Mutation", "Direct Database Access (Must use P10-14 SDKs)"]
    }
}

for p_id, p_data in platforms.items():
    content = f"""---
Authority: Level 2
Parent: Docs/AlphaGrid_Master_Roadmap.md
Children: None
Supersedes: None
Version: 1.0.0
Status: ACTIVE
---

# {p_data['title']}

## 1. Purpose
{p_data['purpose']}

## 2. Extension Policy
This policy dictates what can and cannot be modified within this platform.

### Allowed Changes
"""
    for a in p_data['allowed']:
        content += f"- {a}\n"

    content += "\n### Forbidden Changes\n"
    for f in p_data['forbidden']:
        content += f"- {f}\n"
        
    with open(f"{base_dir}/{p_id}.md", "w") as f:
        f.write(content)

print("Platform Specifications Created.")
