import os
import yaml
import hashlib
from datetime import datetime

GOV_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance"

def freeze_yaml(filepath):
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)
        
    if not isinstance(data, dict) or "checksum" not in data:
        return
        
    # Set dummy checksum to calculate true checksum
    data["checksum"] = "placeholder"
    data["generated_at"] = datetime.utcnow().isoformat() + "Z"
    
    # Calculate md5 hash of the yaml string
    yaml_str = yaml.dump(data, sort_keys=True)
    chksum = hashlib.md5(yaml_str.encode('utf-8')).hexdigest()
    
    data["checksum"] = chksum
    
    with open(filepath, "w") as f:
        yaml.dump(data, f, sort_keys=False)

def freeze_all():
    for root, dirs, files in os.walk(GOV_DIR):
        for file in files:
            if file.endswith(".yaml"):
                freeze_yaml(os.path.join(root, file))
    
    print("Governance freeze complete. All YAML checksums and timestamps updated.")

if __name__ == "__main__":
    freeze_all()
