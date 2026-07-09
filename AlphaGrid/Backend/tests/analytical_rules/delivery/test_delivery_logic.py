import pytest
from Backend.core.analytical_rules.dto.liquidity.price_observation import PriceObservationDTO
from Backend.core.analytical_rules.dto.delivery.delivery_metrics import PriceTraversalDTO
from Backend.core.analytical_rules.capabilities.delivery.delivery_metrics_rule import DeliveryMetricsRule

def test_delivery_metrics_rule():
    rule = DeliveryMetricsRule()
    
    # 4 candles moving upward quickly
    candles = [
        PriceObservationDTO("obs_1", "T1", high=105.0, low=95.0, open=100.0, close=104.0),
        PriceObservationDTO("obs_2", "T2", high=109.0, low=103.0, open=104.0, close=108.0),
        PriceObservationDTO("obs_3", "T3", high=115.0, low=107.0, open=108.0, close=114.0),
        PriceObservationDTO("obs_4", "T4", high=120.0, low=113.0, open=114.0, close=119.0)
    ]
    
    traversal = PriceTraversalDTO(
        start_point_id="start_event",
        end_point_id="end_event",
        observations=candles
    )
    
    metrics = rule.evaluate(traversal)
    
    assert metrics is not None
    assert metrics.candle_count == 4
    assert metrics.time_elapsed == 4
    assert metrics.distance == 19.0 # 119 - 100
    assert metrics.velocity == 19.0 / 4
    
    # Check body ratio and overlap
    # Total body: 4 + 4 + 6 + 5 = 19
    # Total range: 10 + 6 + 8 + 7 = 31
    assert metrics.body_ratio == 19.0 / 31.0
    
    # Overlap between 1-2: min(105, 109) - max(95, 103) = 105 - 103 = 2
    # Overlap between 2-3: min(109, 115) - max(103, 107) = 109 - 107 = 2
    # Overlap between 3-4: min(115, 120) - max(107, 113) = 115 - 113 = 2
    # Total overlap: 6
    assert metrics.overlap_ratio == 6.0 / 31.0
    assert metrics.minimum_overlap == 2.0
