import pytest
from datetime import datetime, timezone
import json

from Backend.core.data_foundation.contracts.schemas import (
    DatasetDefinition, ValidationProfile, MarketType, GapPolicy, DuplicatePolicy,
    SplitPolicy, DividendPolicy, SymbolChangePolicy, DelistingPolicy, MissingVolumePolicy,
    OHLCSchema, FeedQualityReport, QualityScore
)
from Backend.core.data_foundation.storage.storage_layer import MemoryBackend
from Backend.core.data_foundation.storage.parquet_backend import ParquetBackend
from Backend.core.data_foundation.metadata.dataset_builder import DatasetBuilder
from Backend.core.data_foundation.metadata.dataset_catalog import MemoryCatalog, DatasetCatalog
from Backend.core.data_foundation.metadata.ecosystem_tools import DatasetResolver, DatasetLoader, DatasetInspector

@pytest.fixture
def sample_definition():
    return DatasetDefinition(
        dataset_id="temp", provider="TEST", provider_version="1",
        market=MarketType.CRYPTO, asset_type="SPOT", symbol="BTCUSDT",
        exchange="BINANCE", currency="USDT", timezone="UTC", calendar="24x7",
        resolution="1m", adjustment_policy="NONE", corporate_action_policy="RAW",
        fill_policy="NONE", validation_profile="STRICT", start="2024-01-01",
        end="2024-01-02", row_count=0, schema_version="1", compatibility_version="1",
        dataset_hash=""
    )

@pytest.fixture
def strict_profile():
    return ValidationProfile(
        name="STRICT",
        gap_policy=GapPolicy.FAIL, duplicate_policy=DuplicatePolicy.FAIL,
        split_policy=SplitPolicy.FAIL, dividend_policy=DividendPolicy.FAIL,
        symbol_change_policy=SymbolChangePolicy.FAIL, delisting_policy=DelistingPolicy.FAIL,
        missing_volume_policy=MissingVolumePolicy.FAIL
    )

def test_dataset_builder_determinism(sample_definition, strict_profile):
    backend = MemoryBackend()
    builder = DatasetBuilder(backend)
    
    ts = datetime(2024, 1, 1, tzinfo=timezone.utc)
    bar1 = OHLCSchema(ts, 1, 2, 0, 1, 100)
    
    quality = FeedQualityReport("temp", "STRICT", [], [], 0, QualityScore(1,1,1,1,1,1,1), "ACCEPTED")
    
    manifest1 = builder.build_dataset(sample_definition, strict_profile, iter([bar1]), quality)
    manifest2 = builder.build_dataset(sample_definition, strict_profile, iter([bar1]), quality)
    
    assert manifest1.dataset_hash == manifest2.dataset_hash
    assert manifest1.partition_count == 1
    assert manifest1.row_count == 1
    assert manifest1.symbol == "BTCUSDT"

def test_dataset_catalog_discovery(sample_definition, strict_profile):
    backend = MemoryBackend()
    builder = DatasetBuilder(backend)
    
    ts = datetime(2024, 1, 1, tzinfo=timezone.utc)
    bar1 = OHLCSchema(ts, 1, 2, 0, 1, 100)
    
    manifest = builder.build_dataset(sample_definition, strict_profile, iter([bar1]))
    
    catalog_backend = MemoryCatalog()
    catalog = DatasetCatalog(catalog_backend)
    catalog.register(manifest)
    
    resolver = DatasetResolver(catalog)
    resolved = resolver.latest("BTCUSDT", "1m")
    
    assert resolved is not None
    assert resolved.dataset_hash == manifest.dataset_hash
    assert resolved.symbol == "BTCUSDT"
    
def test_dataset_loader(sample_definition, strict_profile):
    backend = MemoryBackend()
    builder = DatasetBuilder(backend)
    
    ts = datetime(2024, 1, 1, tzinfo=timezone.utc)
    bar1 = OHLCSchema(ts, 1, 2, 0, 1, 100)
    
    manifest = builder.build_dataset(sample_definition, strict_profile, iter([bar1]))
    
    loader = DatasetLoader(backend)
    engine = loader.load(manifest)
    
    res = engine.next()
    assert res is not None
    ctx, bar = res
    assert bar.open == 1
    
def test_dataset_inspector(sample_definition, strict_profile):
    backend = MemoryBackend()
    builder = DatasetBuilder(backend)
    
    ts = datetime(2024, 1, 1, tzinfo=timezone.utc)
    bar1 = OHLCSchema(ts, 1, 2, 0, 1, 100)
    
    manifest = builder.build_dataset(sample_definition, strict_profile, iter([bar1]))
    report = DatasetInspector.generate_report(manifest)
    
    assert "Hash: " in report
    assert "Symbol: BTCUSDT | Resolution: 1m" in report
    assert "Rows: 1" in report
