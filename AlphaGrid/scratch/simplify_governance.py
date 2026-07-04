import os
import yaml
import shutil

GOV_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance"

dirs_to_consolidate = ["contracts", "rules", "policies", "lifecycles"]

for d in dirs_to_consolidate:
    dir_path = os.path.join(GOV_DIR, d)
    if not os.path.exists(dir_path):
        continue
    
    consolidated_data = {}
    for filename in os.listdir(dir_path):
        if filename.endswith(".yaml"):
            filepath = os.path.join(dir_path, filename)
            with open(filepath, "r") as f:
                content = yaml.safe_load(f)
                key_name = filename.replace(".yaml", "")
                consolidated_data[key_name] = content
    
    if consolidated_data:
        out_file = os.path.join(GOV_DIR, f"{d}.yaml")
        with open(out_file, "w") as f:
            yaml.dump(consolidated_data, f, sort_keys=False)
            
    # Remove the directory
    shutil.rmtree(dir_path)

print("Simplified governance: Consolidated 30+ YAML files into 4 core files.")
