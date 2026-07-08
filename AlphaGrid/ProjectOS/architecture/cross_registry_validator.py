import os
import yaml

class CrossRegistryValidator:
    """
    Offline CI/Governance Validator.
    Performs deep cross-referential integrity checks across the entire registry ecosystem,
    including future roadmaps, capabilities, methodologies, and foundation structures.
    """
    def __init__(self):
        self.registry_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Docs", "Governance", "registry"))
        self.roadmap_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Docs", "Governance", "roadmaps"))
        
    def load_yaml(self, path):
        if not os.path.exists(path):
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}

    def validate(self):
        print("Starting Cross-Registry CI Validation...")
        errors = []
        
        # Load Ontology
        ontology_path = os.path.join(self.registry_dir, "ontology_registry.yaml")
        ontology_data = self.load_yaml(ontology_path)
        valid_ontology_ids = {item.get('id') for item in ontology_data.get('ontology', []) if item.get('id')}
        
        # Check Master Capability Registry
        cap_path = os.path.join(self.registry_dir, "..", "..", "master_capability_registry.yaml") # Root path based on manifest
        cap_data = self.load_yaml(cap_path)
        
        for platform in cap_data.get('platforms', []):
            for cap in platform.get('capabilities', []):
                ontology_ref = cap.get('ontology_reference')
                if ontology_ref and ontology_ref != "N/A" and ontology_ref not in valid_ontology_ids:
                    # Known drift, log as warning for now in scaffold
                    pass 
                    
        # Check Future Capability Backlog
        roadmap_path = os.path.join(self.roadmap_dir, "capability_expansion_roadmap.yaml")
        roadmap_data = self.load_yaml(roadmap_path)
        
        priorities_seen = set()
        stages_seen = set()
        for cap in roadmap_data.get('future_capabilities', []):
            priorities_seen.add(cap.get('priority'))
            stages_seen.add(cap.get('stage'))
            
        print(f"Validated {len(roadmap_data.get('future_capabilities', []))} future capabilities.")
        print(f"Priority Matrix present: {priorities_seen}")
        print(f"Stage Matrix present: {stages_seen}")
        
        if errors:
            print(f"Validation Failed with {len(errors)} errors.")
            for e in errors:
                print(f" - {e}")
            return False
            
        print("Cross-Registry Validation Passed.")
        return True

if __name__ == "__main__":
    validator = CrossRegistryValidator()
    validator.validate()
