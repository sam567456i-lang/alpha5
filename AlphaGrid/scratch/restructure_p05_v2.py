import os
import shutil
import yaml

BASE_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Backend\platforms\analysis"

exact_folders = [
    "core",
    "registry",
    "factory",
    "engine",
    "metadata",
    "result",
    "validators",
    "benchmarks",
    "tests",
    "docs"
]

for folder in exact_folders:
    os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)

# Clean up old capitalized folders if they exist
old_folders = [
    "Core", "Registry", "Factory", "Engine", "Metadata", "Result",
    "Validator", "Benchmark", "Tests", "Documentation"
]

for old in old_folders:
    old_path = os.path.join(BASE_DIR, old)
    if os.path.exists(old_path) and old not in exact_folders:
        try:
            shutil.rmtree(old_path)
        except Exception:
            pass

# Update platform_manifest.yaml
manifest = {
    "platform_id": "P05",
    "name": "Analysis Platform",
    "version": "1.0.0",
    "owner": "ArchitectureTeam",
    "purpose": "Universal capability discovery and analysis engine.",
    "inputs": ["MarketData"],
    "outputs": ["AnalysisResult"],
    "dependencies": ["P02_Data", "P06_Math_Core"],
    "capabilities": ["Trend", "Momentum", "Volatility", "Volume"],
    "contracts": ["AnalysisContract", "IndicatorContract"],
    "validators": ["Unit", "Integration", "Property"],
    "benchmarks": ["Pandas-TA"],
    "tests": ["pytest"],
    "dashboard": ["Score Panel"],
    "ai": ["AG-EXPLAIN-001"],
    "documentation": ["Docs/"],
    "external_data": ["News"],
    "readiness": {
        "architecture": 90,
        "implementation": 10,
        "validation": 0,
        "performance": 0,
        "documentation": 50,
        "dashboard": 0,
        "ai": 0,
        "research": 0,
        "testing": 0,
        "governance": 100
    },
    "lifecycle": "Implemented",
    "status": "Active"
}

with open(os.path.join(BASE_DIR, "platform_manifest.yaml"), "w") as f:
    yaml.dump(manifest, f, sort_keys=False)

print("Restructured P05 to the exact 10 directories and expanded platform_manifest.yaml.")
