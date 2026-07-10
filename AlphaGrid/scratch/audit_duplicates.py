import os
import re
from collections import defaultdict

def audit():
    targets = {
        "DatasetDefinition": [],
        "SymbolRegistry": [],
        "StorageBackend": [],
        "ValidationProfile": [],
        "MarketRegistry": [],
        "ParquetStore": [], # older name
        "BaseIngestionAdapter": []
    }
    
    for dirpath, dirnames, filenames in os.walk("Backend"):
        if any(ignored in dirpath for ignored in [".git", "__pycache__", "venv"]):
            continue
            
        for file in filenames:
            if not file.endswith(".py"):
                continue
                
            filepath = os.path.join(dirpath, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
            for target in targets.keys():
                if f"class {target}" in content:
                    targets[target].append(filepath)
                    
    print("\n--- DUPLICATION AUDIT RESULTS ---")
    issues_found = False
    for target, paths in targets.items():
        print(f"\n{target} found in {len(paths)} locations:")
        for p in paths:
            print(f"  - {p}")
        if len(paths) > 1:
            print(f"  [!] DUPLICATE DETECTED for {target}")
            issues_found = True
            
    if issues_found:
        print("\nAudit FAILED: Duplicates must be removed before freezing.")
    else:
        print("\nAudit PASSED: No duplicate structures detected.")

if __name__ == "__main__":
    audit()
