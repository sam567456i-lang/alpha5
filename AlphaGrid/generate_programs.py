import os

base_dir = "C:/Users/praka/Documents/Codex/2026-06-30/alphagrid-infinity-x-5-0-master/AlphaGrid/Docs/Programs"
os.makedirs(base_dir, exist_ok=True)

programs = {
    "Knowledge_Platform": "Builds knowledge graphs, RAG, ontology, and research memory.",
    "Research_Platform": "Runs experiments, backtests, validation, and promotion workflows.",
    "AI_Platform": "Provides advisory assistants and agents. Never bypasses deterministic pipeline.",
    "Data_Platform": "Converts external APIs into Curated Data Lakes.",
    "External_Repository": "Audits, maps, and integrates external repos (e.g., Vibe) via adapters.",
    "Operations": "Telemetry, health diagnostics, deployment.",
    "Infrastructure": "K8s, Docker, CI/CD, Secrets.",
    "UI_Platform": "Workspaces, Dashboard widgets, layouts, themes.",
    "Enterprise_Governance": "Traceability, Capability maturity, Technical Debt.",
    "Developer_Platform": "SDKs, Scaffolding tools, CLI."
}

for p_id, p_desc in programs.items():
    content = f"""---
Authority: Level 3
Parent: Docs/AlphaGrid_Master_Roadmap.md
Children: None
Supersedes: None
Version: 1.0.0
Status: ACTIVE
---

# Program: {p_id.replace('_', ' ')}

## 1. Purpose
{p_desc}

## 2. Dependencies
*Defined in `Program_Dependency_Map.md`.*
"""
    with open(f"{base_dir}/{p_id}.md", "w") as f:
        f.write(content)

print("Program Specifications Created.")
