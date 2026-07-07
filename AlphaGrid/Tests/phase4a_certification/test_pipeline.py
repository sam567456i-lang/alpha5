import pytest
import math
from Backend.core.events import EventProvenance, EventPriority
from Backend.dtos.instrument import InstrumentID, AssetClass
from Backend.market_data.validators import DataQualityValidator
from Backend.market_data.normalizers import DefaultNormalizer
from Backend.market_data.derived_data import DerivedDataGenerator

def test_pipeline_determinism():
    validator = DataQualityValidator()
    normalizer = DefaultNormalizer()
    derived_gen = DerivedDataGenerator()
    
    # 1. Raw Payload
    raw_payload_1 = {
        "symbol": "NIFTY",
        "timestamp": 1700000000.0,
        "sequence": 100,
        "price": 20000.0,
        "volume": 50.0
    }
    
    provenance = EventProvenance(
        trace_id="trace_1",
        event_id="evt_1",
        parent_event_id=None,
        origin_service="NSE_WS",
        origin_provider="Zerodha",
        schema_version=1
    )
    
    # 2. Validation
    quality_1 = validator.validate(raw_payload_1)
    assert quality_1.sequence_score == 1.0
    assert quality_1.ohlc_score == 1.0
    
    # 3. Normalization
    canonical_1 = normalizer.normalize(raw_payload_1, quality_1, provenance)
    assert canonical_1.price == 20000.0
    assert canonical_1.volume == 50.0
    
    # 4. Derived Data
    enriched_1 = derived_gen.enrich(canonical_1)
    
    # At tick 1, high=low=close=open=20000
    # True range requires previous close, which is 0 for the first tick, so it uses current price.
    assert enriched_1.derived.hl2 == 20000.0
    assert enriched_1.derived.true_range == 0.0
    assert enriched_1.derived.gap_percent == 0.0
    
    # Tick 2
    raw_payload_2 = {
        "symbol": "NIFTY",
        "timestamp": 1700000001.0,
        "sequence": 101,
        "price": 20100.0,
        "volume": 20.0
    }
    quality_2 = validator.validate(raw_payload_2)
    canonical_2 = normalizer.normalize(raw_payload_2, quality_2, provenance)
    enriched_2 = derived_gen.enrich(canonical_2)
    
    # High is now 20100, Low is 20000.
    assert enriched_2.derived.hl2 == 20050.0
    # True Range = max(H-L, H-Cp, Cp-L) = 100
    assert enriched_2.derived.true_range == 100.0
    # Log Return
    assert math.isclose(enriched_2.derived.log_return, math.log(20100.0 / 20000.0))
    # Session Volume = 50 + 20
    assert enriched_2.derived.session_volume == 70.0

def test_sequence_gap():
    validator = DataQualityValidator()
    
    raw_payload_1 = {"symbol": "RELIANCE", "timestamp": 1700000000.0, "sequence": 50, "price": 2500.0}
    q1 = validator.validate(raw_payload_1)
    assert q1.sequence_score == 1.0
    assert q1.gap_score == 1.0
    
    # Drop sequence 51, receive 52
    raw_payload_2 = {"symbol": "RELIANCE", "timestamp": 1700000002.0, "sequence": 52, "price": 2505.0}
    q2 = validator.validate(raw_payload_2)
    assert q2.sequence_score == 1.0 
    assert q2.gap_score == 0.9  # Gap of 1 sequence (52 - 51) * 0.1 subtracted from 1.0
