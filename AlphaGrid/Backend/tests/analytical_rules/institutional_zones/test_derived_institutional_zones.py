from Backend.core.engine.evidence_quality import EvidenceQualityMetadata
import pytest
from Backend.core.analytical_rules.dto.regions.region_state import RegionState, RegionLifecycleState
from Backend.core.analytical_rules.dto.regions.region_identity import RegionIdentityDTO, RegionType
from Backend.core.analytical_rules.dto.regions.region_geometry import RegionBoundsDTO, RegionGeometryDTO
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus
from Backend.core.analytical_rules.dto.regions.region_relationships import RegionRelationshipType

from Backend.core.analytical_rules.capabilities.institutional_zones.breaker_rule import BreakerRule
from Backend.core.analytical_rules.capabilities.institutional_zones.mitigation_rule import MitigationRule
from Backend.core.analytical_rules.capabilities.institutional_zones.dominance_change_rule import DominanceChangeRule
from Backend.core.analytical_rules.capabilities.institutional_zones.sequential_interaction_rule import SequentialInteractionRule

def _mock_region_state(region_id: str, rtype: RegionType, state: RegionLifecycleState = RegionLifecycleState.CREATED) -> RegionState:
    identity = RegionIdentityDTO(region_id, rtype, ["a", "b"], "regions/test", "none", "fp")
    bounds = RegionBoundsDTO(upper_bound=110.0, lower_bound=100.0)
    geom = RegionGeometryDTO(bounds=bounds, width=3.0, area=30.0, geometry_fingerprint="fp")
    
    return RegionState(
        identity=EvidenceIdentityDTO(f"state_{region_id}", "RegionState", "CAP", "ONT"),
        metadata=EvidenceMetadataDTO("1.0", "1.0", "none", "none", "1.0", "1.0", "fp", {}),
        provenance=EvidenceProvenanceDTO("Engine", "Standard", "T", [], "MKT-1"),
        classification=EvidenceClassification.COMPOSITE,
        interpretation_level=InterpretationLevel.OBJECTIVE,
        validity_status=ValidityStatus.ACTIVE,
        evidence_data={},
        region_identity=identity,
        geometry=geom,
        lifecycle_state=state,
        remaining_height=10.0
    )

def test_breaker_rule():
    rule = BreakerRule()
    invalidated_ob = _mock_region_state("ob_1", RegionType.ORDER_BLOCK, RegionLifecycleState.INVALIDATED)
    struct_evt = EvidenceIdentityDTO("struct_1", "StructureEvent", "CAP", "ONT")
    
    event = rule.evaluate(invalidated_ob, struct_evt)
    assert event is not None
    assert event.region_identity.region_type == RegionType.BREAKER

def test_mitigation_rule():
    rule = MitigationRule()
    invalidated_ob = _mock_region_state("ob_1", RegionType.ORDER_BLOCK, RegionLifecycleState.INVALIDATED)
    struct_evt = EvidenceIdentityDTO("struct_1", "StructureEvent", "CAP", "ONT")
    
    event = rule.evaluate(invalidated_ob, struct_evt)
    assert event is not None
    assert event.region_identity.region_type == RegionType.MITIGATION_BLOCK

def test_dominance_change_rule():
    rule = DominanceChangeRule()
    invalidated_demand = _mock_region_state("demand_1", RegionType.DEMAND_ZONE, RegionLifecycleState.INVALIDATED)
    valid_supply = _mock_region_state("supply_1", RegionType.SUPPLY_ZONE, RegionLifecycleState.CREATED)
    
    event = rule.evaluate(invalidated_demand, valid_supply)
    assert event is not None
    assert event.relationship_type == RegionRelationshipType.DOMINANCE_CHANGE
    assert event.source_region_id == valid_supply.region_identity.region_id
    assert event.target_region_id == invalidated_demand.region_identity.region_id

def test_sequential_interaction_rule():
    rule = SequentialInteractionRule()
    ob_1 = _mock_region_state("ob_1", RegionType.ORDER_BLOCK)
    ob_2 = _mock_region_state("ob_2", RegionType.ORDER_BLOCK)
    
    event = rule.evaluate(ob_1, ob_2)
    assert event is not None
    assert event.relationship_type == RegionRelationshipType.DERIVED_FROM
    assert event.source_region_id == ob_1.region_identity.region_id
    assert event.target_region_id == ob_2.region_identity.region_id
