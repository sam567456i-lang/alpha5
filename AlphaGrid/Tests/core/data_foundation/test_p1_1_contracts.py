import pytest
import json
import hashlib
from datetime import datetime
from Backend.core.data_foundation.contracts.schemas import (
    DatasetDefinition, DatasetManifest, MarketType, ValidationProfile,
    GapPolicy, DuplicatePolicy, SplitPolicy, DividendPolicy, 
    SymbolChangePolicy, DelistingPolicy, MissingVolumePolicy
)
from Backend.core.data_foundation.registry.market_registry import (
    MarketRegistry, MarketMetadata, RegistryException
)
from Backend.core.data_foundation.registry.symbol_registry import (
    SymbolRegistry, SymbolDefinition
)
from Backend.core.data_foundation.storage.storage_layer import (
    MemoryBackend, StorageRegistry, StorageException
)

def test_determinism_dataset_definition():
    def1 = DatasetDefinition(
        dataset_id="ds_001", provider="CSV", provider_version="1.0",
        market=MarketType.EQUITY, asset_type="STOCK", symbol="RELIANCE",
        exchange="NSE", currency="INR", timezone="Asia/Kolkata", calendar="NSE",
        resolution="1m", adjustment_policy="ADJUSTED", corporate_action_policy="STRICT",
        fill_policy="FORWARD", validation_profile="STRICT", start="2023-01-01",
        end="2023-12-31", row_count=100000, schema_version="v1", compatibility_version="1.0", dataset_hash="fake_hash"
    )
    
    def2 = DatasetDefinition(
        dataset_id="ds_001", provider="CSV", provider_version="1.0",
        market=MarketType.EQUITY, asset_type="STOCK", symbol="RELIANCE",
        exchange="NSE", currency="INR", timezone="Asia/Kolkata", calendar="NSE",
        resolution="1m", adjustment_policy="ADJUSTED", corporate_action_policy="STRICT",
        fill_policy="FORWARD", validation_profile="STRICT", start="2023-01-01",
        end="2023-12-31", row_count=100000, schema_version="v1", compatibility_version="1.0", dataset_hash="fake_hash"
    )
    
    hash1 = hashlib.sha256(def1.to_json().encode()).hexdigest()
    hash2 = hashlib.sha256(def2.to_json().encode()).hexdigest()
    assert hash1 == hash2

def test_serialization_dataset_definition():
    def1 = DatasetDefinition(
        dataset_id="ds_001", provider="CSV", provider_version="1.0",
        market=MarketType.CRYPTO, asset_type="PERP", symbol="BTCUSDT",
        exchange="BINANCE", currency="USDT", timezone="UTC", calendar="24x7",
        resolution="1m", adjustment_policy="RAW", corporate_action_policy="NONE",
        fill_policy="ZERO", validation_profile="STRICT", start="2024-01-01",
        end="2024-02-01", row_count=50000, schema_version="v1", compatibility_version="1.0", dataset_hash="fake"
    )
    
    json_str = def1.to_json()
    assert "BTCUSDT" in json_str
    assert "CRYPTO" in json_str

    parsed = json.loads(json_str)
    assert parsed["symbol"] == "BTCUSDT"
    assert parsed["market"] == "CRYPTO"

def test_registry_integrity():
    market_reg = MarketRegistry()
    market = MarketMetadata(
        market_id="m_nse_eq", exchange_id="NSE", market_type=MarketType.EQUITY,
        trading_hours="09:15-15:30", session_rules="strict", holiday_calendar_id="cal_nse",
        timezone_id="tz_ist", currency_id="cur_inr", tick_size_id="ts_0.05",
        lot_size=1.0, asset_type="STOCK"
    )
    market_reg.register(market)
    
    # Duplicate should fail
    with pytest.raises(RegistryException):
        market_reg.register(market)
        
    # Missing should fail
    with pytest.raises(RegistryException):
        market_reg.get("missing_id")
        
    symbol_reg = SymbolRegistry()
    symbol = SymbolDefinition(
        internal_symbol_id="RELIANCE.NS", market_id="m_nse_eq",
        vendor_symbol="RELIANCE", base_asset="RELIANCE", quote_asset="INR"
    )
    symbol_reg.register(symbol)
    
    retrieved = symbol_reg.get("RELIANCE.NS")
    assert retrieved.market_id == "m_nse_eq"

def test_storage_registry():
    reg = StorageRegistry()
    mem = MemoryBackend()
    reg.register("memory", mem)
    
    with pytest.raises(StorageException):
        reg.register("memory", mem)
        
    backend = reg.get("memory")
    backend.write_partition("lake/CSV/EQUITY/STOCK/RELIANCE/1m/2023/01/part.parquet", [{"close": 100}])
    assert backend.exists("lake/CSV/EQUITY/STOCK/RELIANCE/1m/2023/01/part.parquet")
    assert backend.metadata("lake/CSV/EQUITY/STOCK/RELIANCE/1m/2023/01/part.parquet")["row_count"] == 1
