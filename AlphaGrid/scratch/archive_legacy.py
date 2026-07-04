import os
import shutil

P5_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Backend\platforms\analysis"
ARCHIVE_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Backend\archive\analysis"

os.makedirs(ARCHIVE_DIR, exist_ok=True)

core_dirs = [
    "core", "registry", "factory", "engine", "metadata", 
    "result", "validators", "benchmarks", "tests", "docs"
]
core_files = ["platform_manifest.yaml", "test_core.py"]

for item in os.listdir(P5_DIR):
    if item in core_dirs or item in core_files or item == "__pycache__":
        continue
    
    src = os.path.join(P5_DIR, item)
    dst = os.path.join(ARCHIVE_DIR, item)
    
    print(f"Archiving: {item}")
    shutil.move(src, dst)

print("Archival complete.")
