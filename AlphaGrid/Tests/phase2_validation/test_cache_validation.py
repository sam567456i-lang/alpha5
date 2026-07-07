import pytest
import time
from datetime import datetime, timedelta

from Backend.core.cache_service import CacheService

def test_cache_validation_gate_8():
    """
    Gate 8: Cache Validation
    Proves that the Cache Service respects dependency invalidation, 
    dirty state propagation, and TTL expiration correctly.
    """
    cache = CacheService()
    
    # 1. Test basic set/get
    cache.set(layer="indicators", key="SMA_20_NIFTY", data={"sma": 105.0}, dependency_hash="hash_v1", ttl_seconds=10)
    
    # Must retrieve correctly
    res = cache.get(layer="indicators", key="SMA_20_NIFTY")
    assert res is not None
    assert res["sma"] == 105.0
    
    # 2. Test Dependency Invalidation (Dirtying Cache)
    # If the upstream market data feed breaks or is amended, the downstream cache must be invalidated
    cache.invalidate(layer="indicators", key="SMA_20_NIFTY")
    
    # Must return None because it is marked dirty
    res_dirty = cache.get(layer="indicators", key="SMA_20_NIFTY")
    assert res_dirty is None
    
    # 3. Test TTL Expiration
    cache.set(layer="analysis", key="TREND_NIFTY", data={"state": "BULL"}, dependency_hash="hash_v2", ttl_seconds=1) # 1 second TTL
    
    # Should get instantly
    assert cache.get(layer="analysis", key="TREND_NIFTY") is not None
    
    # Mocking Time Expiration by artificially manipulating the entry's last_update backwards by 5 seconds
    entry = cache._layers["analysis"]["TREND_NIFTY"]
    entry.last_update = datetime.utcnow() - timedelta(seconds=5)
    
    # Must return None because it is expired
    assert cache.get(layer="analysis", key="TREND_NIFTY") is None
    
    # Ensure it was physically deleted from the cache dictionary
    assert "TREND_NIFTY" not in cache._layers["analysis"]
