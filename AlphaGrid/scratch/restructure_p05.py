import os
import shutil
import yaml

BASE_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Backend\platforms\analysis"

exact_folders = [
    "Core",
    "Registry",
    "Factory",
    "Engine",
    "Metadata",
    "Result",
    "Validator",
    "Benchmark",
    "Tests",
    "Documentation"
]

for folder in exact_folders:
    os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)

# Generate platform_manifest.yaml
manifest = {
    "schema_version": "1.0",
    "format_version": "1.0",
    "generated_by": "System",
    "generated_at": "2026-07-04T15:00:00Z",
    "checksum": "placeholder",
    "platform_id": "P05",
    "name": "Analysis Platform",
    "owner": "ArchitectureTeam",
    "version": "1.0.0",
    "dependencies": ["P02_Data", "P06_Math_Core", "P08_Indicator_Engine"],
    "subsystems": ["Technical", "Fundamental", "Quantitative", "Macro"],
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
    }
}

with open(os.path.join(BASE_DIR, "platform_manifest.yaml"), "w") as f:
    yaml.dump(manifest, f, sort_keys=False)

print("Created P05 Platform Manifest and scaffolded the 10 exact folders.")
