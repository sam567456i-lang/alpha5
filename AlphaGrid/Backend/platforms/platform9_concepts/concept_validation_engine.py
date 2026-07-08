import os
import yaml
from typing import Dict, Any, List
from Backend.platforms.platform9_concepts.concept_base import BaseConcept
from Backend.platforms.platform9_concepts.semantic_evidence import SemanticEvidence

class ConceptValidationEngine:
    def __init__(self):
        self._load_registries()
        
    def _load_registries(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Docs", "Governance", "registry"))
        
        # Load evidence requirements
        evidence_path = os.path.join(base_dir, "semantic_evidence_registry.yaml")
        with open(evidence_path, 'r', encoding='utf-8') as f:
            self.evidence_reg = yaml.safe_load(f).get("evidence_requirements", {})
            
        # Load capability mappings (to ensure capability exists)
        cap_path = os.path.join(base_dir, "zone_capability_registry.yaml")
        with open(cap_path, 'r', encoding='utf-8') as f:
            self.cap_reg = yaml.safe_load(f).get("capabilities", {})

    def validate_pre_freeze(self, concept: BaseConcept) -> bool:
        """
        Validates a concept against registries before it is frozen and emitted.
        Raises ValueError if validation fails.
        """
        cap_id = concept.concept_id.capability_id
        
        # 1. Capability consistency
        if cap_id not in self.cap_reg:
            raise ValueError(f"Capability {cap_id} not found in zone_capability_registry.yaml")
            
        # 2. Immutable references
        if not concept.source_features:
            raise ValueError(f"Concept {concept.concept_id} has no source features.")
            
        # 3. Evidence validation
        if not concept.semantic_evidence:
            raise ValueError(f"Concept {concept.concept_id} is missing semantic evidence.")
            
        self._validate_evidence(cap_id, concept.semantic_evidence)
        
        # 4. Ontology consistency
        expected_ontology = self.cap_reg[cap_id].get("ontology_id")
        if expected_ontology and concept.concept_id.ontology_id != expected_ontology:
            raise ValueError(f"Ontology mismatch: expected {expected_ontology}, got {concept.concept_id.ontology_id}")
            
        return True

    def _validate_evidence(self, cap_id: str, evidence: SemanticEvidence):
        reqs = self.evidence_reg.get(cap_id)
        if not reqs:
            # If no strict requirements are mapped, allow it to pass for now.
            return
            
        required_criteria = set(reqs.get("required", []))
        provided_criteria = set(evidence.criteria_met)
        
        missing = required_criteria - provided_criteria
        if missing:
            raise ValueError(f"Semantic Evidence missing required criteria for {cap_id}: {missing}")
