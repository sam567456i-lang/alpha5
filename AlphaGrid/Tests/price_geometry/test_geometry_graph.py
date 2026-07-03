import pytest
from datetime import datetime
from Backend.price_geometry.graph.geometry_graph import GeometryGraph
from Backend.price_geometry.objects import Swing, LifecycleState, Liquidity

def test_geometry_graph_addition_and_query():
    graph = GeometryGraph("test_data")
    
    swing1 = Swing(
        id="SWING-H-1",
        version="v1.0.0",
        dataset_id="test_data",
        symbol="BTCUSDT",
        timeframe="1D",
        timestamp=datetime(2026, 1, 1),
        price=150.0,
        is_high=True
    )
    
    swing2 = Swing(
        id="SWING-H-2",
        version="v1.0.0",
        dataset_id="test_data",
        symbol="BTCUSDT",
        timeframe="1D",
        timestamp=datetime(2026, 1, 5),
        price=150.0,
        is_high=True
    )
    
    eqh = Liquidity(
        id="EQH-1",
        version="v1.0.0",
        dataset_id="test_data",
        symbol="BTCUSDT",
        timeframe="1D",
        timestamp=datetime(2026, 1, 5),
        price=150.0,
        parent_ids=["SWING-H-1", "SWING-H-2"],
        pool_type="EQH",
        lifecycle_state=LifecycleState.CONFIRMED
    )
    
    graph.add_object(swing1)
    graph.add_object(swing2)
    graph.add_object(eqh)
    
    # Check edges
    assert graph._graph.has_edge("SWING-H-1", "EQH-1")
    assert graph._graph.has_edge("SWING-H-2", "EQH-1")
    
    # Query active pools
    pools = graph.get_active_liquidity_pools()
    assert len(pools) == 1
    assert pools[0].id == "EQH-1"
    
    # Update state
    graph.update_object_state("EQH-1", LifecycleState.INVALIDATED)
    pools = graph.get_active_liquidity_pools()
    assert len(pools) == 0
