import pytest
from datetime import datetime, timezone, timedelta
import hashlib
from typing import Iterator

from Backend.core.data_foundation.contracts.schemas import (
    ValidationProfile, GapPolicy, DuplicatePolicy, SplitPolicy,
    DividendPolicy, SymbolChangePolicy, DelistingPolicy, MissingVolumePolicy,
    OHLCSchema, DatasetManifest, MarketType
)
from Backend.core.data_foundation.registry.market_registry import MarketMetadata
from Backend.core.data_foundation.validation.feed_quality import FeedQualityEngine
from Backend.core.data_foundation.replay.sequential_replay import SequentialReplayEngine
from Backend.core.data_foundation.storage.storage_layer import MemoryBackend

@pytest.fixture
def base_profile():
    return ValidationProfile(
        name="STRICT",
        gap_policy=GapPolicy.FAIL,
        duplicate_policy=DuplicatePolicy.FAIL,
        split_policy=SplitPolicy.FAIL,
        dividend_policy=DividendPolicy.FAIL,
        symbol_change_policy=SymbolChangePolicy.FAIL,
        delisting_policy=DelistingPolicy.FAIL,
        missing_volume_policy=MissingVolumePolicy.FAIL
    )

@pytest.fixture
def crypto_market():
    return MarketMetadata("CRYPTO_MKT", "BINANCE", MarketType.CRYPTO, "24x7", "N/A", "N/A", "UTC", "USDT", "TS1", 1.0, "PERP")

@pytest.fixture
def equity_market():
    return MarketMetadata("EQ_MKT", "NSE", MarketType.EQUITY, "09:15-15:30", "N/A", "N/A", "IST", "INR", "TS1", 1.0, "STOCK")

def test_duplicate_timestamp_rejection(base_profile, crypto_market):
    engine = FeedQualityEngine("ds1", base_profile, crypto_market, timedelta(minutes=1))
    
    ts = datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc)
    bar1 = OHLCSchema(ts, 100, 101, 99, 100, 1000)
    bar2 = OHLCSchema(ts, 101, 102, 100, 101, 2000)
    
    stream = iter([bar1, bar2])
    valid_stream, report = engine.validate_stream(stream)
    results = list(valid_stream)
    
    rep = engine.generate_report()
    assert len(results) == 1
    assert "Duplicate timestamp" in rep.errors[0]
    assert rep.status == "REJECTED"
    assert rep.quality_score.duplicates == 0.5

def test_weekend_bar_rejection(base_profile, equity_market):
    engine = FeedQualityEngine("ds2", base_profile, equity_market, timedelta(days=1))
    
    # Jan 6, 2024 is a Saturday
    ts = datetime(2024, 1, 6, 10, 0, tzinfo=timezone.utc)
    bar = OHLCSchema(ts, 100, 101, 99, 100, 1000)
    
    stream = iter([bar])
    valid_stream, report = engine.validate_stream(stream)
    results = list(valid_stream)
    
    rep = engine.generate_report()
    assert len(results) == 0
    assert "Weekend bar detected" in rep.errors[0]
    assert rep.status == "REJECTED"
    assert rep.quality_score.calendar == 0.0

def test_timeframe_resolution_gap(base_profile, crypto_market):
    engine = FeedQualityEngine("ds3", base_profile, crypto_market, timedelta(minutes=60))
    
    ts1 = datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc)
    ts2 = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc) # 2-hour gap on 1H resolution
    
    bar1 = OHLCSchema(ts1, 100, 101, 99, 100, 1000)
    bar2 = OHLCSchema(ts2, 100, 101, 99, 100, 1000)
    
    stream = iter([bar1, bar2])
    valid_stream, report = engine.validate_stream(stream)
    results = list(valid_stream)
    
    rep = engine.generate_report()
    assert len(results) == 1 # Second bar dropped because GapPolicy is FAIL
    assert "Gap detected" in rep.errors[0]
    assert rep.status == "REJECTED"

def test_replay_determinism():
    manifest = DatasetManifest(
        dataset_hash="fake_hash", row_count=2, missing_bars=0, duplicate_bars=0,
        first_timestamp="2024-01-01", last_timestamp="2024-01-01", average_gap_seconds=60.0,
        largest_gap_seconds=60.0, resolution="1m", start="2024", end="2024",
        provider="CSV", schema_version="1", calendar="NSE", timezone="UTC",
        generation_time="NOW", software_version="1", quality_report=None
    )
    
    ts = datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc)
    bar1 = OHLCSchema(ts, 100, 101, 99, 100, 1000)
    bar2 = OHLCSchema(ts + timedelta(minutes=1), 101, 102, 100, 101, 2000)
    
    backend = MemoryBackend()
    # Mocking partition write
    backend.write_partition("fake_hash_part_1", [bar1, bar2])
    
    engine1 = SequentialReplayEngine(manifest, backend)
    hash1 = hashlib.sha256()
    while True:
        res = engine1.next()
        if not res: break
        ctx, bar = res
        hash1.update(bar.timestamp.isoformat().encode())
        
    engine2 = SequentialReplayEngine(manifest, backend)
    hash2 = hashlib.sha256()
    while True:
        res = engine2.next()
        if not res: break
        ctx, bar = res
        hash2.update(bar.timestamp.isoformat().encode())
        
    assert hash1.hexdigest() == hash2.hexdigest()
    assert engine1.position() == engine2.position() == 2
