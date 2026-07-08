import pytest
from datetime import datetime, timezone
from Backend.platforms.platform9_concepts.plugins.gap_concepts import FVGConceptPlugin
from Backend.platforms.platform9_concepts.zone_features import ZoneFeature
from Backend.platforms.platform9_concepts.feature_base import FeatureType
from Backend.shared_domain.contracts.zones.zone_dtos import ZoneDTO, ZoneGeometryDTO, ZoneIdentityDTO, ZoneMetadataDTO, ZoneLifecycleStatus
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

def test_plugin_is_stateless_and_deterministic(context):
    plugin = FVGConceptPlugin()
    
    zone = create_mock_zone()
    feature_type = FeatureType(id="ZONE_FEATURE", name="Zone Feature", family="SPATIAL")
    feature = ZoneFeature(
        context=context, feature_id="", feature_type=feature_type, version=1, 
        quality=1.0, confidence=1.0, produced_at=datetime.now(timezone.utc),
        zone_dto=zone
    )
    
    # 1. Determinism and Statelessness
    concepts1 = plugin.extract([feature], context)
    concepts2 = plugin.extract([feature], context)
    
    assert len(concepts1) == len(concepts2) == 1
    
    # Manually freeze to get hash since the plugin doesn't freeze them (Factory does)
    c1 = concepts1[0]
    c2 = concepts2[0]
    c1.freeze()
    c2.freeze()
    
    assert c1.lineage_hash == c2.lineage_hash
    assert c1.fingerprint_hash == c2.fingerprint_hash
    
    # 2. Replay Compatibility
    # Replay contexts should not alter core outputs
    replay_context = ExecutionContext(
        session_id="S1", trace_id="T1", correlation_id="C1", instrument_id="AAPL",
        environment="TEST", runtime_mode="TEST", exchange="NASDAQ", provider="MOCK",
        market="NASDAQ", timezone="UTC", sequence_id=1, is_replay=True, build_version="1.0"
    )
    concepts_replay = plugin.extract([feature], replay_context)
    cr = concepts_replay[0]
    cr.freeze()
    
    # Note: Context may alter the hash if we decide context is part of determinism. 
    # Currently context is part of Concept, but lineage hash does NOT hash the context object itself in `freeze()`.
    # It hashes source features and evidence. So replay hash must be identical.
    assert c1.lineage_hash == cr.lineage_hash

def test_plugin_immutable_outputs(context):
    plugin = FVGConceptPlugin()
    zone = create_mock_zone()
    feature_type = FeatureType(id="ZONE_FEATURE", name="Zone Feature", family="SPATIAL")
    feature = ZoneFeature(
        context=context, feature_id="", feature_type=feature_type, version=1, 
        quality=1.0, confidence=1.0, produced_at=datetime.now(timezone.utc),
        zone_dto=zone
    )
    
    concepts = plugin.extract([feature], context)
    c1 = concepts[0]
    c1.freeze()
    
    with pytest.raises(TypeError):
        c1.confidence = 0.99
