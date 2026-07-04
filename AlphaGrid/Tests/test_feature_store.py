"""Production unit tests for the Feature Store (PR-2)."""

import pytest
from decimal import Decimal
from datetime import datetime, timezone
from typing import Any, Dict, List

from Shared.models.market import MarketSnapshot
from Backend.features.base import AbstractFeature
from Backend.features.registry import FeatureRegistry
from Backend.features.engine import FeatureEngine
from Backend.features.cache import FeatureCache
from Backend.reference.legacy.features.trend import SMAFeature, EMAFeature
from Backend.features.momentum import ROCFeature, RSIFeature
from Backend.features.volatility import ATRFeature, RelativeVolumeFeature


def _make_snapshot(close: float, volume: int = 1000, idx: int = 0, high: float = None, low: float = None, open_: float = None) -> MarketSnapshot:
    if high is None: high = close + 1
    if low is None: low = max(0.01, close - 1)
    if open_ is None: open_ = close
    return MarketSnapshot(
        symbol='TEST', exchange='NSE', instrument_type='EQ',
        last_price=Decimal(str(close)), open=Decimal(str(open_)),
        high=Decimal(str(high)), low=Decimal(str(low)),
        close=Decimal(str(close)), volume=volume,
        timestamp=datetime(2025, 1, 1, idx % 24, idx // 24 if idx // 24 <= 28 else 1, 0, tzinfo=timezone.utc)
    )

# ---------------------------------------------------------------------------
# Stubs for Registry Tests
# ---------------------------------------------------------------------------

class StubFeatureA(AbstractFeature):
    @classmethod
    def get_name(cls) -> str: return "A"
    @classmethod
    def get_version(cls) -> str: return "v1"
    def compute(self, snapshot, deps): return 1

class StubFeatureB(AbstractFeature):
    @classmethod
    def get_name(cls) -> str: return "B"
    @classmethod
    def get_version(cls) -> str: return "v1"
    @classmethod
    def get_dependencies(cls) -> List[str]: return ["A"]
    @classmethod
    def warmup_period(cls) -> int: return 5
    def compute(self, snapshot, deps): return deps["A"] + 1

class StubFeatureC(AbstractFeature):
    @classmethod
    def get_name(cls) -> str: return "C"
    @classmethod
    def get_version(cls) -> str: return "v1"
    @classmethod
    def get_dependencies(cls) -> List[str]: return ["B"]
    def compute(self, snapshot, deps): return deps["B"] + 1

class CyclicX(AbstractFeature):
    @classmethod
    def get_name(cls) -> str: return "X"
    @classmethod
    def get_version(cls) -> str: return "v1"
    @classmethod
    def get_dependencies(cls) -> List[str]: return ["Y"]
    def compute(self, snapshot, deps): return 0

class CyclicY(AbstractFeature):
    @classmethod
    def get_name(cls) -> str: return "Y"
    @classmethod
    def get_version(cls) -> str: return "v1"
    @classmethod
    def get_dependencies(cls) -> List[str]: return ["X"]
    def compute(self, snapshot, deps): return 0


# ---------------------------------------------------------------------------
# Registry Tests
# ---------------------------------------------------------------------------

class TestFeatureRegistry:
    def test_registration_success(self):
        reg = FeatureRegistry()
        reg.register(StubFeatureA)
        assert len(reg) == 1
        assert "A" in reg.get_all_names()

    def test_registration_duplicate_fails(self):
        reg = FeatureRegistry()
        reg.register(StubFeatureA)
        with pytest.raises(ValueError, match="Duplicate feature name"):
            reg.register(StubFeatureA)

    def test_registration_invalid_type_fails(self):
        reg = FeatureRegistry()
        class NotAFeature: pass
        with pytest.raises(TypeError):
            reg.register(NotAFeature) # type: ignore

    def test_build_dag_success(self):
        reg = FeatureRegistry()
        reg.register(StubFeatureC)
        reg.register(StubFeatureA)
        reg.register(StubFeatureB)
        
        dag = reg.build_dag()
        names = [cls.get_name() for cls in dag]
        
        # A must come before B, B must come before C
        assert names.index("A") < names.index("B")
        assert names.index("B") < names.index("C")

    def test_build_dag_missing_dependency(self):
        reg = FeatureRegistry()
        reg.register(StubFeatureB) # Depends on A, which is missing
        with pytest.raises(ValueError, match="is not registered"):
            reg.build_dag()

    def test_build_dag_circular_dependency(self):
        reg = FeatureRegistry()
        reg.register(CyclicX)
        reg.register(CyclicY)
        with pytest.raises(ValueError, match="Circular dependency"):
            reg.build_dag()

    def test_get_feature_success(self):
        reg = FeatureRegistry()
        reg.register(StubFeatureA)
        assert reg.get_feature("A") == StubFeatureA

    def test_get_feature_missing(self):
        reg = FeatureRegistry()
        with pytest.raises(ValueError, match="is not registered"):
            reg.get_feature("Missing")

    def test_get_max_warmup(self):
        reg = FeatureRegistry()
        assert reg.get_max_warmup() == 0
        reg.register(StubFeatureA) # warmup 0
        assert reg.get_max_warmup() == 0
        reg.register(StubFeatureB) # warmup 5
        assert reg.get_max_warmup() == 5


# ---------------------------------------------------------------------------
# Feature Implementation Tests
# ---------------------------------------------------------------------------

class TestSMAFeature:
    def test_sma_constant_price(self):
        feat = SMAFeature(period=5)
        
        # Warmup
        for i in range(4):
            assert feat.compute(_make_snapshot(10.0, idx=i), {}) is None
            
        # Ready
        assert feat.compute(_make_snapshot(10.0, idx=4), {}) == 10.0
        assert feat.compute(_make_snapshot(10.0, idx=5), {}) == 10.0

    def test_sma_trend(self):
        feat = SMAFeature(period=3)
        feat.compute(_make_snapshot(10.0, idx=0), {})
        feat.compute(_make_snapshot(20.0, idx=1), {})
        assert feat.compute(_make_snapshot(30.0, idx=2), {}) == 20.0 # (10+20+30)/3
        assert feat.compute(_make_snapshot(40.0, idx=3), {}) == 30.0 # (20+30+40)/3


class TestEMAFeature:
    def test_ema_constant_price(self):
        feat = EMAFeature(period=5)
        
        # Warmup (SMA initialized)
        for i in range(5):
            assert feat.compute(_make_snapshot(10.0, idx=i), {}) is None
            
        # First real EMA value uses the previous SMA (which is 10)
        assert feat.compute(_make_snapshot(10.0, idx=5), {}) == 10.0


class TestROCFeature:
    def test_roc_flat(self):
        feat = ROCFeature(lookback=3)
        for i in range(3):
            assert feat.compute(_make_snapshot(100.0, idx=i), {}) is None
            
        assert feat.compute(_make_snapshot(100.0, idx=3), {}) == 0.0

    def test_roc_rising(self):
        feat = ROCFeature(lookback=2)
        feat.compute(_make_snapshot(100.0, idx=0), {})
        feat.compute(_make_snapshot(105.0, idx=1), {})
        # Price 2 steps ago was 100, current is 110
        assert feat.compute(_make_snapshot(110.0, idx=2), {}) == pytest.approx(0.1)


class TestRSIFeature:
    def test_rsi_rising(self):
        feat = RSIFeature(period=14)
        for i in range(14):
            # Consistently rising
            feat.compute(_make_snapshot(100.0 + i, idx=i), {})
        val = feat.compute(_make_snapshot(115.0, idx=14), {})
        assert val == 100.0 # No down days

    def test_rsi_falling(self):
        feat = RSIFeature(period=14)
        for i in range(14):
            # Consistently falling
            feat.compute(_make_snapshot(100.0 - i, idx=i), {})
        val = feat.compute(_make_snapshot(85.0, idx=14), {})
        assert val == 0.0 # No up days


class TestATRFeature:
    def test_atr_constant_range(self):
        feat = ATRFeature(period=5)
        # range = 2 (high=11, low=9)
        for i in range(4):
            assert feat.compute(_make_snapshot(10.0, high=11.0, low=9.0, idx=i), {}) is None
            
        val = feat.compute(_make_snapshot(10.0, high=11.0, low=9.0, idx=4), {})
        assert val == 2.0


class TestRelativeVolumeFeature:
    def test_rvol_constant(self):
        feat = RelativeVolumeFeature(period=3)
        # First 3 bars
        assert feat.compute(_make_snapshot(10.0, volume=1000, idx=0), {}) is None
        assert feat.compute(_make_snapshot(10.0, volume=1000, idx=1), {}) is None
        assert feat.compute(_make_snapshot(10.0, volume=1000, idx=2), {}) is None
        
        # 4th bar
        val = feat.compute(_make_snapshot(10.0, volume=1000, idx=3), {})
        assert val == 1.0
        
        # 5th bar (surge)
        val = feat.compute(_make_snapshot(10.0, volume=2000, idx=4), {})
        assert val == 2.0


# ---------------------------------------------------------------------------
# Feature Engine Integration Tests
# ---------------------------------------------------------------------------

class TestFeatureEngine:
    def test_engine_process_respects_warmup(self):
        reg = FeatureRegistry()
        reg.register(StubFeatureA)
        reg.register(StubFeatureB)
        
        engine = FeatureEngine(reg)
        
        for i in range(5):
            results = engine.process(_make_snapshot(10.0))
            assert results["A"] == 1 # Warmup 0
            assert results["B"] is None # Warmup 5
            
        # 6th call
        results = engine.process(_make_snapshot(10.0))
        assert results["A"] == 1
        assert results["B"] == 2 # 1 + 1
