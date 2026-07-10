import os

base_dir = "C:/Users/praka/Documents/Codex/2026-06-30/alphagrid-infinity-x-5-0-master/AlphaGrid/Docs/Platforms"

platforms_ownership = {
    "Platform10": {
        "owns": ["Objective evidence", "Measurements", "Relationships", "Observations", "Canonical graphs"],
        "cannot_own": ["Bias", "Narratives", "Decisions", "Risk", "Trading signals"]
    },
    "Platform11": {
        "owns": ["Methodology Profiles", "Subjective Interpretations", "Projections", "Evaluator logic"],
        "cannot_own": ["Objective indicator generation", "Decisions", "Execution logic"]
    },
    "Platform12": {
        "owns": ["Decision Vectors", "Execution Candidates", "Conflict Resolution", "Strategic Plans"],
        "cannot_own": ["Order routing", "Broker abstraction", "Evidence extraction"]
    },
    "Platform13": {
        "owns": ["Tactical Order Sequences", "Broker implementations", "Slippage models"],
        "cannot_own": ["Strategic decision making", "Risk validation (Layer 4 handles Risk)"]
    },
    "Platform14": {
        "owns": ["Attribution", "Drift Detection", "ML/RL Optimization", "Calibration"],
        "cannot_own": ["Mutating Historical Evidence", "Direct live execution routing"]
    },
    "Platform15": {
        "owns": ["Presentation", "REST APIs", "Dashboards", "External SDKs"],
        "cannot_own": ["Business logic", "State Mutation", "Direct database access"]
    }
}

for p_id, p_data in platforms_ownership.items():
    filepath = f"{base_dir}/{p_id}.md"
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
            
        ownership_block = "\n## 3. Strict Layer Ownership\n\n### Owns\n"
        for o in p_data["owns"]:
            ownership_block += f"- {o}\n"
            
        ownership_block += "\n### Cannot Own\n"
        for co in p_data["cannot_own"]:
            ownership_block += f"- {co}\n"
            
        with open(filepath, 'w') as f:
            f.write(content + ownership_block)
            
print("Updated Platform Specifications with Layer Ownership.")
