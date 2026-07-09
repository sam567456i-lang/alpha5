import pytest
from Backend.core.analytical_rules.dto.liquidity.liquidity_anchor import SwingAnchor
from Backend.core.analytical_rules.capabilities.liquidity.equal_detector import EqualHighDetector, EqualLowDetector, EqualDetectorPolicy
from Backend.core.analytical_rules.capabilities.liquidity.equal_lifecycle_engine import EqualPrimitiveLifecycleEngine

def test_equal_high_detector():
    policy = EqualDetectorPolicy(price_variance_threshold=1.5, anchor_types_allowed=["NODE_STRUCTURE_SWING_HIGH"])
    detector = EqualHighDetector(policy)
    engine = EqualPrimitiveLifecycleEngine()
    
    anchors = [
        SwingAnchor(anchor_id="anchor_1", price=100.0, timestamp="T1", origin_type="NODE_STRUCTURE_SWING_HIGH", swing_id="swing_1", source_detector="test", source_policy="test", source_event="test", origin_graph_namespace="test"),
        SwingAnchor(anchor_id="anchor_2", price=101.0, timestamp="T2", origin_type="NODE_STRUCTURE_SWING_HIGH", swing_id="swing_2", source_detector="test", source_policy="test", source_event="test", origin_graph_namespace="test"),
        SwingAnchor(anchor_id="anchor_3", price=105.0, timestamp="T3", origin_type="NODE_STRUCTURE_SWING_HIGH", swing_id="swing_3", source_detector="test", source_policy="test", source_event="test", origin_graph_namespace="test"),
        SwingAnchor(anchor_id="anchor_4", price=100.5, timestamp="T4", origin_type="NODE_STRUCTURE_SWING_HIGH", swing_id="swing_4", source_detector="test", source_policy="test", source_event="test", origin_graph_namespace="test")
    ]
    
    events = detector.detect(anchors)
    
    # 100.0, 101.0, and 100.5 have a max variance of 1.0 (between 100 and 101), which is <= 1.5. 
    # They should form a single cluster of 3 anchors.
    # 105.0 is too far away.
    assert len(events) == 1
    event = events[0]
    
    assert set(event.anchor_ids) == {"anchor_1", "anchor_2", "anchor_4"}
    assert event.anchor_count == 3
    assert event.average_price == (100.0 + 101.0 + 100.5) / 3
    assert event.price_variance == 1.0
    
    state = engine.process_high_event(event)
    assert state.anchor_count == 3
    assert set(state.anchor_ids) == {"anchor_1", "anchor_2", "anchor_4"}

def test_equal_low_detector():
    policy = EqualDetectorPolicy(price_variance_threshold=0.5, anchor_types_allowed=["NODE_STRUCTURE_SWING_LOW"])
    detector = EqualLowDetector(policy)
    engine = EqualPrimitiveLifecycleEngine()
    
    anchors = [
        SwingAnchor(anchor_id="anchor_1", price=50.0, timestamp="T1", origin_type="NODE_STRUCTURE_SWING_LOW", swing_id="swing_1", source_detector="test", source_policy="test", source_event="test", origin_graph_namespace="test"),
        SwingAnchor(anchor_id="anchor_2", price=49.8, timestamp="T2", origin_type="NODE_STRUCTURE_SWING_LOW", swing_id="swing_2", source_detector="test", source_policy="test", source_event="test", origin_graph_namespace="test"),
        SwingAnchor(anchor_id="anchor_3", price=49.6, timestamp="T3", origin_type="NODE_STRUCTURE_SWING_LOW", swing_id="swing_3", source_detector="test", source_policy="test", source_event="test", origin_graph_namespace="test")
    ]
    
    events = detector.detect(anchors)
    
    # Max variance of all three is 50.0 - 49.6 = 0.4.
    # 0.4 <= 0.5. They should form a single cluster of 3 anchors.
    assert len(events) == 1
    event = events[0]
    
    assert set(event.anchor_ids) == {"anchor_1", "anchor_2", "anchor_3"}
    assert event.anchor_count == 3
    assert event.price_variance == pytest.approx(0.4)
    
    state = engine.process_low_event(event)
    assert state.anchor_count == 3
