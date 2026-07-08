import uuid
from typing import List
from Backend.platforms.platform9_concepts.concept_base import BaseConcept
from Backend.platforms.platform9_concepts.concept_validation_engine import ConceptValidationEngine

class ConceptFactory:
    """
    Centralized factory for creating, validating, and freezing Concepts.
    Plugins should yield raw/unfrozen BaseConcept objects, and the Factory takes ownership of them.
    """
    def __init__(self):
        self.validator = ConceptValidationEngine()
        
    def assemble_and_freeze(self, raw_concepts: List[BaseConcept]) -> List[BaseConcept]:
        """
        Takes raw concepts from plugins, validates them against governance rules,
        calculates their confidence score using the registry, freezes them, and returns them.
        """
        valid_concepts = []
        for concept in raw_concepts:
            # 1. Validate against governance rules
            try:
                self.validator.validate_pre_freeze(concept)
            except ValueError as e:
                # Log invalid concept and drop it
                print(f"Concept Validation Failed: {e}")
                continue
                
            # 2. Assign root ID if not present
            if not concept.concept_id.root_concept_id:
                # In python, dataclasses are immutable if frozen=True.
                # ConceptID is frozen=True. We must replace it.
                from dataclasses import replace
                new_id = replace(concept.concept_id, root_concept_id=f"ROOT-{uuid.uuid4().hex[:8]}")
                # We can't do replace directly on frozen concept, but it's not frozen yet.
                concept.concept_id = new_id

            # 3. Freeze concept (generates lineage hash and fingerprint)
            concept.freeze()
            valid_concepts.append(concept)
            
        return valid_concepts
