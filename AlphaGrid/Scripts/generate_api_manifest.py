import os
import json
import hashlib

base_dir = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
manifest_path = os.path.join(base_dir, "Docs", "Governance", "api_freeze_manifest.json")

locked_files = [
    # APIs
    "Backend/math/public/__init__.py",
    "Backend/indicator_engine/__init__.py",
    "Backend/features/__init__.py",
    
    # Schemas
    "Backend/validation/dtos.py",
    "master_capability_registry.yaml",
    "Docs/Documentation_Registry.yaml",
    "Backend/validation/validation_registry.py",
    
    # Governance & Architecture
    "Docs/Governance/Wave_Lifecycle.md",
    "Docs/Architecture/capability_dependency_graph.md",
    
    # Dataset and Profiles
    "Datasets/dataset_manifest.json",
    "Docs/Evidence/2026/EV-TEMP/validation_manifest.json",
]

# We also want to hash the ADR directory
locked_dirs = [
    "Docs/ADRs",
    "Docs/adr"
]

manifest = {}

for rel_path in locked_files:
    full_path = os.path.join(base_dir, os.path.normpath(rel_path))
    if os.path.exists(full_path):
        with open(full_path, "rb") as f:
            content = f.read()
            manifest[rel_path] = hashlib.sha256(content).hexdigest()
    else:
        print(f"Warning: {full_path} not found")

for rel_dir in locked_dirs:
    dir_path = os.path.join(base_dir, os.path.normpath(rel_dir))
    if os.path.exists(dir_path):
        for root, _, files in os.walk(dir_path):
            for file in sorted(files):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir).replace("\\", "/")
                with open(full_path, "rb") as f:
                    manifest[rel_path] = hashlib.sha256(f.read()).hexdigest()

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump({"locked_apis": manifest}, f, indent=4)
    
print(f"Generated {manifest_path} with {len(manifest)} locked APIs.")
