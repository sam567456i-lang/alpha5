import os
import shutil
import glob

BASE = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Backend\platforms\analysis"

def move(src, dst):
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"Moved {src} to {dst}")

# 1. Global Layer Moves
move(os.path.join(BASE, "engine", "engine.py"), os.path.join(BASE, "engine.py"))
move(os.path.join(BASE, "engine", "pipeline.py"), os.path.join(BASE, "pipeline.py"))
move(os.path.join(BASE, "registry", "registry_loader.py"), os.path.join(BASE, "registry.py")) # Check if this is the name
move(os.path.join(BASE, "core", "dto.py"), os.path.join(BASE, "contracts.py"))
move(os.path.join(BASE, "factory", "factory.py"), os.path.join(BASE, "factory.py")) # I will bring factory to the root too

# Try moving registry.py if registry_loader didn't exist
move(os.path.join(BASE, "registry", "registry.py"), os.path.join(BASE, "registry.py"))

# 2. Family Refactors
families = ["trend", "momentum", "volatility", "extremum", "volume"]

for fam in families:
    fam_dir = os.path.join(BASE, fam)
    if not os.path.exists(fam_dir):
        continue
        
    analyses_dir = os.path.join(fam_dir, "analyses")
    os.makedirs(analyses_dir, exist_ok=True)
    
    # Move all *_analysis.py scripts to analyses/
    scripts = glob.glob(os.path.join(fam_dir, "*_analysis.py"))
    for script in scripts:
        shutil.move(script, os.path.join(analyses_dir, os.path.basename(script)))
        
    # Create empty stubs for local architecture
    with open(os.path.join(fam_dir, "engine.py"), "w") as f: f.write("# Local engine\n")
    with open(os.path.join(fam_dir, "registry.py"), "w") as f: f.write("# Local registry\n")
    with open(os.path.join(fam_dir, "validators.py"), "w") as f: f.write("# Local validators\n")
    with open(os.path.join(fam_dir, "benchmark.py"), "w") as f: f.write("# Local benchmark\n")
    
print("File structural moves completed.")

# 3. Replace Imports
def replace_in_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()
        
    original = content
    content = content.replace("Backend.platforms.analysis.core.dto", "Backend.platforms.analysis.contracts")
    content = content.replace("Backend.platforms.analysis.engine.engine", "Backend.platforms.analysis.engine")
    content = content.replace("Backend.platforms.analysis.engine.pipeline", "Backend.platforms.analysis.pipeline")
    content = content.replace("Backend.platforms.analysis.factory.factory", "Backend.platforms.analysis.factory")
    content = content.replace("Backend.platforms.analysis.registry.registry_loader", "Backend.platforms.analysis.registry")
    content = content.replace("Backend.platforms.analysis.registry.registry", "Backend.platforms.analysis.registry")
    
    # fix the paths for tests that import from trend.xxx instead of trend.analyses.xxx
    for fam in families:
        content = content.replace(f"Backend.platforms.analysis.{fam}.", f"Backend.platforms.analysis.{fam}.analyses.")
        
    # fix the issue where it replaces too much, e.g. analysis.trend.analyses.analyses
    content = content.replace(f".analyses.analyses.", f".analyses.")
    
    if original != content:
        with open(filepath, "w") as f:
            f.write(content)
        print(f"Updated imports in {filepath}")

for root, _, files in os.walk(BASE):
    for file in files:
        if file.endswith(".py"):
            replace_in_file(os.path.join(root, file))
            
print("Refactor complete.")
