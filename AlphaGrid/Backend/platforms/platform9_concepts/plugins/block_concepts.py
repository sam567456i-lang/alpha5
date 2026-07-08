import yaml
import os
from typing import List, Any
from Backend.platforms.platform9_concepts.concept_framework import ConceptPlugin
from Backend.platforms.platform9_concepts.concept_base import BaseConcept, ConceptID, ConceptCategory, ConceptType
from Backend.platforms.platform9_concepts.zone_features import ZoneFeature
from Backend.platforms.platform9_concepts.semantic_evidence import SemanticEvidence
from Backend.core.state import ExecutionContext

class OrderBlockConceptPlugin(ConceptPlugin):
    def __init__(self):
        super().__init__()
        self._load_capability_mapping()

    def _load_capability_mapping(self):
        registry_path = os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "..", "..", "Docs", "Governance", "registry", "zone_capability_registry.yaml"
        )
        with open(registry_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            self.ob_mapping = data.get("capabilities", {}).get("CAP-OB-01", {})
            self.base_zone_type = self.ob_mapping.get("base_zone_type", "BLOCK_ZONE")

    def extract(self, features: List[Any], context: ExecutionContext) -> List[BaseConcept]:
        concepts = []
        for feature in features:
            if not isinstance(feature, ZoneFeature):
                continue
                
            zone = feature.zone_dto
            if zone.identity.zone_type != self.base_zone_type:
                continue
                
            # Evidence collection
            evidence = SemanticEvidence(
                evidence_id=f"EVID-OB-{zone.identity.zone_id}",
                criteria_met=["structural_break", "volume_node_support"],
                supporting_metrics={"strength": zone.strength},
                supporting_zone_id=zone.identity.zone_id,
                detector_version=zone.metadata.registry_version
            )
            
            c_id = ConceptID(
                category=ConceptCategory.SPATIAL,
                type=ConceptType.ORDER_BLOCK,
                capability_id="CAP-OB-01",
                ontology_id=zone.identity.ontology_id,
                version="1.0.0"
            )
            
            concept = BaseConcept(
                concept_id=c_id,
                source_features=[feature],
                semantic_evidence=evidence,
                description=f"Order Block Concept",
                context=context
            )
            concepts.append(concept)
            
        return concepts

class BreakerConceptPlugin(ConceptPlugin):
    def __init__(self):
        super().__init__()
        self._load_capability_mapping()

    def _load_capability_mapping(self):
        registry_path = os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "..", "..", "Docs", "Governance", "registry", "zone_capability_registry.yaml"
        )
        with open(registry_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            self.brk_mapping = data.get("capabilities", {}).get("CAP-BRK-01", {})
            self.base_zone_type = self.brk_mapping.get("base_zone_type", "BLOCK_ZONE")

    def extract(self, features: List[Any], context: ExecutionContext) -> List[BaseConcept]:
        concepts = []
        for feature in features:
            if not isinstance(feature, ZoneFeature):
                continue
                
            zone = feature.zone_dto
            if zone.identity.zone_type != self.base_zone_type:
                continue
                
            # Assume Breaker requires the zone to be INVALIDATED or mitigated through
            if zone.status.value not in ["INVALIDATED", "MITIGATED"]:
                continue
                
            evidence = SemanticEvidence(
                evidence_id=f"EVID-BRK-{zone.identity.zone_id}",
                criteria_met=["failed_block", "explosive_shift"],
                supporting_metrics={"freshness": zone.freshness},
                supporting_zone_id=zone.identity.zone_id,
                detector_version=zone.metadata.registry_version
            )
            
            c_id = ConceptID(
                category=ConceptCategory.SPATIAL,
                type=ConceptType.BREAKER_BLOCK,
                capability_id="CAP-BRK-01",
                ontology_id=zone.identity.ontology_id,
                version="1.0.0"
            )
            
            concept = BaseConcept(
                concept_id=c_id,
                source_features=[feature],
                semantic_evidence=evidence,
                description=f"Breaker Block Concept",
                context=context
            )
            concepts.append(concept)
            
        return concepts
