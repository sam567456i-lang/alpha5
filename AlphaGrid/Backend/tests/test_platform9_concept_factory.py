import pytest
from datetime import datetime, timezone
import yaml

from Backend.shared_domain.contracts.zones.zone_dtos import ZoneDTO, ZoneGeometryDTO, ZoneIdentityDTO, ZoneMetadataDTO, ZoneLifecycleStatus
from Backend.platforms.platform9_concepts.zone_features import ZoneFeature
from Backend.platforms.platform9_concepts.feature_base import FeatureType
from Backend.platforms.platform9_concepts.plugins.gap_concepts import FVGConceptPlugin
from Backend.platforms.platform9_concepts.concept_factory import ConceptFactory
from Backend.core.state import ExecutionContext

def create_mock_zone() -> ZoneDTO:
    identity = ZoneIdentityDTO(
        zone_id="z1", zone_version=1, previous_version_id=None, root_zone_id="z1",
        zone_type="GAP_ZONE", ontology_id="ONT-001", capability_id="CAP-001",
        market="NASDAQ", asset_class="Equities", exchange="NASDAQ", symbol="AAPL",
        timeframe="H1", session_id="RTH", source_detector="MockDetector", registry_version="1.0.0"
    )
    geometry = ZoneGeometryDTO(upper_price=100.0, lower_price=90.0)
    metadata = ZoneMetadataDTO(
        registry_version="1.0.0", fingerprint_hash="hash123", created_by="test",
        detector="MockDetector", latency_ms=1.0, confidence_model="N/A", freshness_model="N/A"
    )
    return ZoneDTO(
        identity=identity, geometry=geometry, metadata=metadata,
        status=ZoneLifecycleStatus.ACTIVE, created_at=datetime.now(timezone.utc)
    )

@pytest.fixture
def context():
    return ExecutionContext(
        session_id="S1", trace_id="T1", correlation_id="C1", instrument_id="AAPL",
        environment="TEST", runtime_mode="TEST", exchange="NASDAQ", provider="MOCK",
        market="NASDAQ", timezone="UTC", sequence_id=1, is_replay=False, build_version="1.0"
    )

def test_concept_factory_freezes_and_fingerprints(context):
    zone = create_mock_zone()
    feature_type = FeatureType(id="ZONE_FEATURE", name="Zone Feature", family="SPATIAL")
    feature = ZoneFeature(
        context=context, feature_id="", feature_type=feature_type, version=1, 
        quality=1.0, confidence=1.0, produced_at=datetime.now(timezone.utc),
        zone_dto=zone
    )
    
    plugin = FVGConceptPlugin()
    raw_concepts = plugin.extract([feature], context)
    
    # Factory
    factory = ConceptFactory()
    frozen_concepts = factory.assemble_and_freeze(raw_concepts)
    
    assert len(frozen_concepts) == 1
    concept = frozen_concepts[0]
    
    # Assert frozen
    assert concept._is_frozen is True
    assert concept.lineage_hash is not None
    assert concept.fingerprint_hash is not None
    
    # Assert Root ID assigned
    assert concept.concept_id.root_concept_id is not None
    assert concept.concept_id.root_concept_id.startswith("ROOT-")

def test_concept_validation_engine_drops_invalid():
    # If a plugin returns a concept missing required semantic evidence, 
    # the factory should drop it (validator will raise ValueError).
    from Backend.platforms.platform9_concepts.concept_base import BaseConcept, ConceptID, ConceptCategory, ConceptType
    from Backend.platforms.platform9_concepts.semantic_evidence import SemanticEvidence
    
    bad_concept = BaseConcept(
        concept_id=ConceptID(
            category=ConceptCategory.SPATIAL, type=ConceptType.FAIR_VALUE_GAP,
            capability_id="CAP-FVG-01", ontology_id="ONT-001"
        ),
        # missing source features
        source_features=[],
        # missing full semantic evidence
        semantic_evidence=SemanticEvidence(
            evidence_id="EVID-1",
            criteria_met=["imbalance"], # MISSING displacement!
            supporting_metrics={}, supporting_zone_id="z1", detector_version="1.0"
        )
    )
    
    factory = ConceptFactory()
    frozen_concepts = factory.assemble_and_freeze([bad_concept])
    
    assert len(frozen_concepts) == 0 # dropped by validation!
