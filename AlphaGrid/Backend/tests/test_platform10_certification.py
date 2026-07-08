import pytest
from datetime import datetime
from Backend.platforms.platform9_concepts.concept_base import (
    ConceptID, ConceptCategory, ConceptType, ConceptSeverity, BaseConcept
)
from Backend.platforms.platform9_concepts.concept_registry import ConceptRegistry
from Backend.platforms.platform9_concepts.concept_framework import ConceptCompiler
from Backend.platforms.platform10_methodologies.plugins.market_structure_concepts import MarketRegimeConcept
from Backend.platforms.platform9_concepts.feature_base import FloatFeature, BaseFeature, FeatureType
from Backend.core.state import ExecutionContext

class MockConcept(BaseConcept):
    pass

def get_test_context() -> ExecutionContext:
    return ExecutionContext(
        session_id="N/A", trace_id="N/A", correlation_id="N/A", instrument_id="N/A",
        environment="TEST", runtime_mode="TEST", exchange="N/A", provider="N/A",
        market="N/A", timezone="UTC", sequence_id=0, is_replay=False, build_version="1.0"
    )

def test_concept_id_hashing():
    cid1 = ConceptID(ConceptCategory.STRUCTURE, ConceptType.BULL_MARKET, "1.0.0")
    cid2 = ConceptID(ConceptCategory.STRUCTURE, ConceptType.BULL_MARKET, "1.0.0")
    assert cid1 == cid2
    assert hash(cid1) == hash(cid2)

def test_base_concept_immutability():
    ctx = get_test_context()
    ftype = FeatureType(id="test_ft", name="Test", family="Test")
    
    feature = FloatFeature(
        feature_id="f1",
        feature_type=ftype,
        version=1,
        quality=1.0,
        confidence=1.0,
        produced_at=datetime.utcnow(),
        context=ctx,
        feature_value=0.8
    )
    # Mocking freeze for testing concept immutability
    # In Platform9, BaseFeature is already frozen, but let's assume it behaves as normal frozen dataclass.
    
    cid = ConceptID(ConceptCategory.STRUCTURE, ConceptType.BULL_MARKET)
    c_ctx = get_test_context()
    
    concept = MockConcept(
        concept_id=cid,
        source_features=[feature],
        context=c_ctx
    )
    
    # Pre-freeze mutations allowed
    concept.description = "Updated"
    assert concept.description == "Updated"
    
    concept.freeze()
    
    with pytest.raises(TypeError):
        concept.description = "Cannot modify"
        
    assert concept.lineage_hash is not None

def test_compiler_pipeline():
    ctx = get_test_context()
    ftype = FeatureType(id="test_ft", name="Test", family="Test")
    
    f1 = FloatFeature(
        feature_id="f1",
        feature_type=ftype,
        version=1,
        quality=1.0,
        confidence=1.0,
        produced_at=datetime.utcnow(),
        context=ctx,
        feature_value=0.8
    )
    f2 = FloatFeature(
        feature_id="f2",
        feature_type=ftype,
        version=1,
        quality=1.0,
        confidence=1.0,
        produced_at=datetime.utcnow(),
        context=ctx,
        feature_value=0.2
    )
    
    c_ctx = get_test_context()
    compiler = ConceptCompiler()
    
    # f1 is bullish (>0.5), f2 is not
    concepts = compiler.compile([f1, f2], c_ctx)
    
    assert len(concepts) == 1
    assert isinstance(concepts[0], MarketRegimeConcept)
    assert concepts[0].concept_id.type == ConceptType.BULL_MARKET
    assert getattr(concepts[0], "_is_frozen") is True
    assert concepts[0].lineage_hash is not None
