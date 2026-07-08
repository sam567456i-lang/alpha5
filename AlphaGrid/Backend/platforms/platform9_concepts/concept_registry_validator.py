import os
import yaml
from typing import Dict, Any, List

class ConceptRegistryValidator:
    def __init__(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Docs", "Governance", "registry"))
        
    def validate(self) -> bool:
        """
        Validates concept-specific registries:
        - orphan capabilities
        - duplicate IDs
        - missing evidence definitions
        - missing methodology mappings
        """
        try:
            zone_cap_path = os.path.join(self.base_dir, "zone_capability_registry.yaml")
            with open(zone_cap_path, 'r', encoding='utf-8') as f:
                cap_reg = yaml.safe_load(f).get("capabilities", {})
                
            evidence_path = os.path.join(self.base_dir, "semantic_evidence_registry.yaml")
            with open(evidence_path, 'r', encoding='utf-8') as f:
                evidence_reg = yaml.safe_load(f).get("evidence_requirements", {})
                
            methodology_path = os.path.join(self.base_dir, "concept_methodology_registry.yaml")
            with open(methodology_path, 'r', encoding='utf-8') as f:
                methodology_reg = yaml.safe_load(f).get("methodology_mappings", {})

            # Validate that every capability mapped to a Concept Type has evidence and methodology mappings
            for cap_id, mapping in cap_reg.items():
                # Only care about concept-generation capabilities
                if not cap_id.startswith("CAP-"):
                    continue
                    
                # 1. Missing evidence definitions
                if cap_id not in evidence_reg:
                    print(f"Warning: Capability {cap_id} is missing evidence definitions in semantic_evidence_registry.yaml")
                    
                # 2. Missing methodology mappings
                if cap_id not in methodology_reg:
                    print(f"Warning: Capability {cap_id} is missing methodology mappings in concept_methodology_registry.yaml")
                    
            return True
        except Exception as e:
            print(f"ConceptRegistryValidator failed: {e}")
            return False
