import os
import yaml
import glob
import re

class ConceptCoverageAuditor:
    def __init__(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Docs", "Governance", "registry"))
        self.plugins_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "plugins"))
        
    def audit(self):
        zone_cap_path = os.path.join(self.base_dir, "zone_capability_registry.yaml")
        with open(zone_cap_path, 'r', encoding='utf-8') as f:
            cap_reg = yaml.safe_load(f).get("capabilities", {})
            
        # Find all capabilities that are meant for concepts
        concept_caps = {cap_id: data for cap_id, data in cap_reg.items() if cap_id.startswith("CAP-")}
        
        # Scan plugins for implemented capabilities
        implemented_caps = set()
        plugin_files = glob.glob(os.path.join(self.plugins_dir, "*.py"))
        
        for pfile in plugin_files:
            with open(pfile, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extremely simple regex to find string literals matching CAP-
                matches = re.findall(r'"(CAP-[A-Z]+-\d+)"', content)
                for m in matches:
                    implemented_caps.add(m)
                    
        print("\n--- Concept Capability Coverage Audit ---")
        for cap_id, data in concept_caps.items():
            concept_type = data.get("concept_type", "Unknown")
            if cap_id in implemented_caps:
                print(f"[OK] {cap_id} ({concept_type}) is implemented in a plugin.")
            else:
                print(f"[WARNING] {cap_id} ({concept_type}) exists in registry but has no plugin implementation!")
        print("-----------------------------------------\n")

if __name__ == "__main__":
    auditor = ConceptCoverageAuditor()
    auditor.audit()
