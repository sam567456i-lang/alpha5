import os
import shutil

BASE_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
GOV_DIR = os.path.join(BASE_DIR, "Governance")
DOCS_DIR = os.path.join(BASE_DIR, "Docs")

folders = [
    "manifests",
    "registry",
    "taxonomy",
    "schemas",
    "contracts",
    "lifecycles",
    "rules",
    "policies",
    "templates",
    "freeze",
    "reports",
    "generated",
    "changelogs",
    "platform_manifests"
]

for folder in folders:
    os.makedirs(os.path.join(GOV_DIR, folder), exist_ok=True)

# 1. Revert ADRs
adr_gov = os.path.join(GOV_DIR, "adr")
adr_docs = os.path.join(DOCS_DIR, "ADRs")
os.makedirs(adr_docs, exist_ok=True)
if os.path.exists(adr_gov):
    for f in os.listdir(adr_gov):
        shutil.move(os.path.join(adr_gov, f), os.path.join(adr_docs, f))
    shutil.rmtree(adr_gov)

# 2. Move existing YAMLs to subdirectories
moves = {
    "master_taxonomy.yaml": "taxonomy",
    "master_capability_registry.yaml": "registry",
    "validation_registry.yaml": "registry",
    "repository_manifest.yaml": "manifests"
}

for file, subfolder in moves.items():
    src = os.path.join(GOV_DIR, file)
    if os.path.exists(src):
        shutil.move(src, os.path.join(GOV_DIR, subfolder, file))

# 3. Clean up CSV and other old files
csv_file = os.path.join(GOV_DIR, "master_capability_matrix.csv")
if os.path.exists(csv_file):
    os.remove(csv_file)

print("Scaffolding complete.")
