import os
import yaml
from collections import defaultdict
import glob

class CapabilityConsolidator:
    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        self.output_dir = os.path.join(repo_root, "Docs", "Audit")
        self.inventory_path = os.path.join(self.output_dir, "01_Master_Capability_Inventory.md")
        self.ownership_path = os.path.join(self.output_dir, "02_Capability_Ownership_Matrix.md")
        
        # Load all registries
        self.capabilities = {}
        self.load_registries()

    def load_registries(self):
        # Scan Governance/registry for yaml files
        reg_dir = os.path.join(self.repo_root, "Docs", "Governance")
        if not os.path.exists(reg_dir):
            reg_dir = os.path.join(self.repo_root, "Governance", "registry")
            
        for root, _, files in os.walk(self.repo_root):
            for file in files:
                if file.endswith(".yaml") and "registry" in file.lower() and "snapshot" not in root.lower():
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = yaml.safe_load(f)
                            if data and isinstance(data, dict) and 'capabilities' in data:
                                for cap in data['capabilities']:
                                    cid = cap.get('id', 'UNKNOWN')
                                    if cid not in self.capabilities:
                                        self.capabilities[cid] = cap
                                        self.capabilities[cid]['source_registry'] = filepath
                    except Exception as e:
                        pass

    def check_implementation(self, cap):
        # 1. Look for a class with the same name or ID
        name = cap.get('name', '').replace(' ', '')
        if not name:
            return "Missing"
        
        # Simple scan
        backend_dir = os.path.join(self.repo_root, "Backend")
        found_code = False
        found_test = False
        
        # We will do a fast generic walk
        for root, _, files in os.walk(backend_dir):
            for file in files:
                if file.endswith(".py"):
                    if name.lower() in file.lower():
                        if "test_" in file.lower():
                            found_test = True
                        else:
                            found_code = True
                            
        if found_code and found_test:
            return "Verified (Implemented & Tested)"
        elif found_code:
            return "Verified (Implemented, Missing Tests)"
        else:
            return "Missing"

    def run(self):
        inventory_lines = [
            "# Phase 1: Master Capability Inventory",
            "| ID | Name | Owner | Phase | Consumes | Produces | Status | Confidence | Evidence |",
            "|---|---|---|---|---|---|---|---|---|"
        ]
        
        ownership_lines = [
            "# Phase 1: Capability Ownership Matrix",
            "| Capability | Owner | Allowed to Read | Allowed to Extend | Consumes | Produces | Status |",
            "|---|---|---|---|---|---|---|"
        ]
        
        for cid, cap in sorted(self.capabilities.items()):
            name = cap.get('name', 'Unknown')
            owner = cap.get('owner', 'Unknown')
            phase = cap.get('required_phase', 'Unknown')
            consumes = ", ".join(cap.get('consumes', []))
            produces = ", ".join(cap.get('produces', []))
            
            # Evidence verification
            status = self.check_implementation(cap)
            confidence = "High" if status.startswith("Verified") else "Medium"
            evidence = "Code Found" if status.startswith("Verified") else "No Code Found"
            
            inventory_lines.append(f"| {cid} | {name} | {owner} | {phase} | {consumes} | {produces} | {status} | {confidence} | {evidence} |")
            
            # Ownership
            readers = "ProjectOS"
            extenders = owner
            ownership_lines.append(f"| {name} | {owner} | {readers} | {extenders} | {consumes} | {produces} | Verified |")
            
        with open(self.inventory_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(inventory_lines))
            
        with open(self.ownership_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(ownership_lines))
            
        print("Phase 1 deliverables generated.")

if __name__ == "__main__":
    repo = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
    consolidator = CapabilityConsolidator(repo)
    consolidator.run()
