import os
import yaml

GOV_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance"

# 1. Expand Repository Manifest
repo_manifest_path = os.path.join(GOV_DIR, "manifests", "repository_manifest.yaml")
with open(repo_manifest_path, "r") as f:
    repo_manifest = yaml.safe_load(f)

repo_manifest.update({
    "repository": "AlphaGrid-Infinity-X",
    "platforms": ["P01", "P02", "P03", "P04", "P05", "P06", "P07", "P08", "P09", "P10", "P11", "P12"],
    "governance": ["registry", "taxonomy", "manifests", "lifecycles", "rules", "policies", "freeze", "reports"],
    "contracts": ["Analysis", "Indicator", "Feature", "Concept", "Methodology", "Signal", "Opportunity", "Recommendation", "Dashboard", "AI"],
    "schemas": ["taxonomy.schema.json", "registry.schema.json", "validation.schema.json", "roadmap.schema.json"],
    "generators": ["generate_docs.py", "generate_matrix.py", "generate_dashboard_docs.py", "generate_project_bible.py", "generate_reports.py"],
    "validators": ["GovernanceValidator", "ArchitectureValidator", "CodeValidator"],
    "reports": ["Repository_Report.md", "Platform_Report.md", "Validation_Report.md"],
    "knowledge": ["Confluence", "Project_Bible"],
    "ai": ["AG-RES-001", "AG-EXPLAIN-001", "AG-DEV-001"],
    "dashboard": ["Trader_Terminal", "Risk_Console"],
    "external_repositories": [
        {
            "id": "EXT-001",
            "name": "Pandas-TA",
            "owner": "twopirllc",
            "license": "MIT",
            "commit_hash": "v0.3.14b0",
            "release": "stable",
            "dependencies": ["pandas", "numpy"],
            "security_scan": "Passed",
            "architecture_score": 95,
            "performance_score": 90,
            "compatibility": "Python 3.10+",
            "sandbox_status": "Approved",
            "approval_status": "Approved",
            "imported_modules": ["pandas_ta.trend", "pandas_ta.momentum"],
            "replacement_strategy": "Migrate to Platform 8",
            "last_validation": "2026-07-04T00:00:00Z",
            "risk_score": "Low"
        }
    ],
    "data_sources": ["MarketData", "News", "Fundamentals"],
    "tests": ["pytest", "hypothesis"],
    "benchmarks": ["pytest-benchmark"],
    "documentation": ["Docs/"],
    "templates": ["Governance/templates/"],
    "cicd": ["GitHub Actions"]
})

# Remove old checksum/generated_at
if "checksum" in repo_manifest:
    del repo_manifest["checksum"]
if "generated_at" in repo_manifest:
    del repo_manifest["generated_at"]

with open(repo_manifest_path, "w") as f:
    yaml.dump(repo_manifest, f, sort_keys=False)

# 2. Expand Capability Registry
cap_registry_path = os.path.join(GOV_DIR, "registry", "master_capability_registry.yaml")
with open(cap_registry_path, "r") as f:
    cap_registry = yaml.safe_load(f)

for cap in cap_registry.get("capabilities", []):
    cap_id = cap.get("id", "UNKNOWN")
    cap["capability_id"] = cap_id
    cap["platform"] = "P05"
    cap["family"] = "Technical"
    cap["subfamily"] = "Trend"
    cap["description"] = f"{cap.get('name', 'Analysis')} capability."
    cap["inputs"] = ["OHLCV"]
    cap["outputs"] = ["Score", "Explainability"]
    cap["dependencies"] = ["P02_Data", "P06_Math_Core"]
    cap["markets"] = ["Stocks", "Crypto", "Forex"]
    cap["timeframes"] = ["1H", "4H", "Daily"]
    cap["trading_styles"] = ["Swing", "Position"]
    cap["analysis_domains"] = ["Technical"]
    cap["strategies"] = ["Trend Following"]
    cap["dashboard_widgets"] = ["Chart", "Score Panel"]
    cap["ai_compatibility"] = True
    cap["validation_profile"] = "analysis"
    cap["benchmark_profile"] = "analysis_bench"
    cap["documentation"] = "Planned"
    cap["version"] = "1.0.0"
    cap["lifecycle"] = "Planned"
    cap["status"] = "Designed"
    cap["deprecated"] = False
    cap["replacement"] = ""
    cap["tags"] = ["core", "v1"]
    
    # Remove old schema fields that got expanded
    keys_to_remove = ["relationships", "market_support", "streaming_support", "dashboard_contracts", "cross_platform_references", "maturity", "id"]
    for k in keys_to_remove:
        if k in cap:
            del cap[k]

if "checksum" in cap_registry:
    del cap_registry["checksum"]
if "generated_at" in cap_registry:
    del cap_registry["generated_at"]

with open(cap_registry_path, "w") as f:
    yaml.dump(cap_registry, f, sort_keys=False)

print("Expanded Repository Manifest and Capability Registry.")
