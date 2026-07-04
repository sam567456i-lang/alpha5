import os
import json
import hashlib

base_dir = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
manifest_path = os.path.join(base_dir, "Docs", "Governance", "api_freeze_manifest.json")

locked_files = [
    "Backend/math/public/__init__.py",
    "Backend/indicator_engine/__init__.py",
    "Backend/features/__init__.py",
    "Backend/validation/dtos.py",
    "master_capability_registry.yaml"
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

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump({"locked_apis": manifest}, f, indent=4)
    
print(f"Generated {manifest_path} with {len(manifest)} locked APIs.")
