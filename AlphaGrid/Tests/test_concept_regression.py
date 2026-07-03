import pytest
from datetime import datetime
from Backend.concepts.generators.market_structure import MarketStructureConceptGenerator
from Backend.price_geometry.cache import GeometryCache
from Backend.price_geometry.objects import Structure, LifecycleState

def test_market_structure_concept_generator():
    """Validates deterministic translation of geometry into atomic concept states."""
    cache = GeometryCache()
    ts = datetime.utcnow()
    
    # Inject a mock structure
    struct = Structure(
        id="CHOCH-BULL-1",
        version="v1.0.0",
        dataset_id="test",
        symbol="BTCUSDT",
        timeframe="1H",
        timestamp=ts,
        price=50000.0,
        structure_type="CHOCH",
        is_bullish=True,
        lifecycle_state=LifecycleState.CONFIRMED
    )
    cache.add(struct)
    
    generator = MarketStructureConceptGenerator()
    concept = generator.evaluate(timestamp=ts, feature_values={"close": 50100.0}, geometry_cache=cache)
    
    assert concept is not None
    assert concept.inputs["price"] == 50100.0
    
    latest_structure = concept.inputs["latest_structure"]
    assert latest_structure is not None
    assert latest_structure["type"] == "CHOCH"
    assert latest_structure["is_bullish"] is True
    
    # Ensure dependencies are tracked
    assert "CHOCH-BULL-1" in concept.geometry_dependencies
