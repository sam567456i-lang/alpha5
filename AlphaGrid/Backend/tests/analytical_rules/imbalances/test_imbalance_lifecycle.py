from Backend.core.engine.evidence_quality import EvidenceQualityMetadata
import pytest
from Backend.core.analytical_rules.dto.regions.region_identity import RegionIdentityDTO, RegionType
from Backend.core.analytical_rules.dto.regions.region_geometry import RegionBoundsDTO
from Backend.core.analytical_rules.dto.regions.region_events import RegionDetectedEventDTO, RegionReferenceInteractionEventDTO, RegionReferenceType
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

from Backend.core.analytical_rules.capabilities.regions.region_lifecycle_engine import RegionLifecycleEngine
from Backend.core.analytical_rules.dto.regions.region_state import RegionLifecycleState

def _create_mock_detected_event(region_id: str) -> RegionDetectedEventDTO:
    identity = RegionIdentityDTO(
        region_id=region_id,
        region_type=RegionType.FVG,
        anchor_ids=["obs1", "obs2", "obs3"],
        graph_namespace="regions/fvg",
        policy_checksum="none",
        geometry_fingerprint="100-110"
    )
    bounds = RegionBoundsDTO(upper_bound=110.0, lower_bound=100.0)
    
    return RegionDetectedEventDTO(
        identity=EvidenceIdentityDTO(
            evidence_id="evt_1",
            evidence_type="RegionDetectedEvent",
            capability_id="CAP-REGION-DETECTION",
            ontology_id="ONT-REGION-DETECTED-EVENT"
        ),
        metadata=EvidenceMetadataDTO("1.0", "1.0", "none", "none", "1.0", "1.0", "evt_1", {}),
        provenance=EvidenceProvenanceDTO("FVGDetectionRule", "Standard", "T", ["obs1", "obs2", "obs3"], "MKT-1"),
        classification=EvidenceClassification.COMPOSITE,
        interpretation_level=InterpretationLevel.OBJECTIVE,
        validity_status=ValidityStatus.ACTIVE,
        evidence_data={},
        quality=EvidenceQualityMetadata(confidence=1.0, coverage=1.0, freshness=0.0, latency=0.0, source_quality=1.0, sample_size=1, stability=1.0),
        superseded_by=None,
        region_identity=identity,
        bounds=bounds,
        width=3.0,
        anchor_observation_ids=["obs1", "obs2", "obs3"]
    )

def _create_mock_interaction_event(region_id: str, ref_type: RegionReferenceType) -> RegionReferenceInteractionEventDTO:
    identity = RegionIdentityDTO(
        region_id=region_id,
        region_type=RegionType.FVG,
        anchor_ids=["obs1", "obs2", "obs3"],
        graph_namespace="regions/fvg",
        policy_checksum="none",
        geometry_fingerprint="100-110"
    )
    return RegionReferenceInteractionEventDTO(
        identity=EvidenceIdentityDTO("evt_2", "RegionReferenceInteractionEvent", "CAP", "ONT"),
        metadata=EvidenceMetadataDTO("1.0", "1.0", "none", "none", "1.0", "1.0", "evt_2", {}),
        provenance=EvidenceProvenanceDTO("RegionInteractionRule", "Standard", "T", ["obs4"], "MKT-1"),
        classification=EvidenceClassification.COMPOSITE,
        interpretation_level=InterpretationLevel.OBJECTIVE,
        validity_status=ValidityStatus.ACTIVE,
        evidence_data={},
        quality=EvidenceQualityMetadata(confidence=1.0, coverage=1.0, freshness=0.0, latency=0.0, source_quality=1.0, sample_size=1, stability=1.0),
        superseded_by=None,
        region_identity=identity,
        reference_type=ref_type,
        interaction_price=105.0,
        interaction_observation_id="obs4"
    )

def test_imbalance_lifecycle_creation():
    engine = RegionLifecycleEngine()
    detected_event = _create_mock_detected_event("region_1")
    
    state = engine.process_event(detected_event)
    
    assert state is not None
    assert state.lifecycle_state == RegionLifecycleState.CREATED
    assert state.remaining_height == 10.0
    assert state.geometry.bounds.upper_bound == 110.0

def test_imbalance_lifecycle_partial_fill():
    engine = RegionLifecycleEngine()
    engine.process_event(_create_mock_detected_event("region_1"))
    
    partial_fill_evt = _create_mock_interaction_event("region_1", RegionReferenceType.FILL_PARTIAL)
    state = engine.process_event(partial_fill_evt)
    
    assert state is not None
    assert state.lifecycle_state == RegionLifecycleState.PARTIALLY_FILLED
    assert state.remaining_height == 5.0 # Mock engine cuts it in half

def test_imbalance_lifecycle_full_fill():
    engine = RegionLifecycleEngine()
    engine.process_event(_create_mock_detected_event("region_1"))
    
    full_fill_evt = _create_mock_interaction_event("region_1", RegionReferenceType.FILL_FULL)
    state = engine.process_event(full_fill_evt)
    
    assert state is not None
    assert state.lifecycle_state == RegionLifecycleState.FULLY_FILLED
    assert state.remaining_height == 0.0

    # Test ignoring subsequent events after FULLY_FILLED
    ignored_state = engine.process_event(full_fill_evt)
    assert ignored_state is None
