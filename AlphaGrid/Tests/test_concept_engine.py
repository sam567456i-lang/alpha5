"""Production unit tests for Concept Engine (PR-3)."""

import pytest
from datetime import datetime, timezone

from Backend.concepts.base import Concept
from Backend.concepts.registry import ConceptRegistry
from Backend.concepts.engine import ConceptEngine
from Backend.concepts.generators.momentum import MomentumConceptGenerator
from Backend.concepts.generators.trend import TrendConceptGenerator
from Backend.concepts.generators.volatility import VolatilityConceptGenerator


# ---------------------------------------------------------------------------
# Concept Engine & Registry Tests
# ---------------------------------------------------------------------------

class TestConceptImmutability:
    def test_concept_is_frozen(self):
        c = Concept(id="test", version="v1", timestamp=datetime.now(),
                    confidence=1.0, inputs={}, generator="TestGen")
        with pytest.raises(AttributeError):
            c.confidence = 0.5  # type: ignore

class TestConceptRegistry:
    def test_registration(self):
        reg = ConceptRegistry()
        reg.register(MomentumConceptGenerator)
        assert len(reg.get_all()) == 1

# ---------------------------------------------------------------------------
# Generator Tests
# ---------------------------------------------------------------------------

class TestMomentumConceptGenerator:
    def setup_method(self):
        self.gen = MomentumConceptGenerator()
        self.ts = datetime(2025, 1, 1, tzinfo=timezone.utc)

    def test_overbought(self):
        c = self.gen.evaluate(self.ts, {"ROC_5": 0.03, "RSI_14": 80.0})
        assert c.inputs["state"] == "OVERBOUGHT"
        assert c.confidence == 0.8

    def test_oversold(self):
        c = self.gen.evaluate(self.ts, {"ROC_5": -0.03, "RSI_14": 20.0})
        assert c.inputs["state"] == "OVERSOLD"
        assert c.confidence == 0.8

    def test_neutral(self):
        c = self.gen.evaluate(self.ts, {"ROC_5": 0.001, "RSI_14": 50.0})
        assert c.inputs["state"] == "NEUTRAL"
        assert c.confidence == 0.3

class TestTrendConceptGenerator:
    def setup_method(self):
        self.gen = TrendConceptGenerator()
        self.ts = datetime(2025, 1, 1, tzinfo=timezone.utc)

    def test_bullish(self):
        # spread > 0.5%
        c = self.gen.evaluate(self.ts, {"EMA_20": 101.0, "SMA_20": 100.0})
        assert c.inputs["state"] == "BULLISH_TREND"

    def test_bearish(self):
        # spread < -0.5%
        c = self.gen.evaluate(self.ts, {"EMA_20": 99.0, "SMA_20": 100.0})
        assert c.inputs["state"] == "BEARISH_TREND"

    def test_no_trend(self):
        c = self.gen.evaluate(self.ts, {"EMA_20": 100.1, "SMA_20": 100.0})
        assert c.inputs["state"] == "NO_TREND"
        assert c.confidence == 0.2

class TestVolatilityConceptGenerator:
    def setup_method(self):
        self.gen = VolatilityConceptGenerator()
        self.ts = datetime(2025, 1, 1, tzinfo=timezone.utc)

    def test_high_volatility(self):
        # Needs 3 bars of ATR history to expand
        self.gen.evaluate(self.ts, {"ATR_14": 1.0, "RelativeVolume_5": 1.0})
        self.gen.evaluate(self.ts, {"ATR_14": 1.1, "RelativeVolume_5": 1.0})
        c = self.gen.evaluate(self.ts, {"ATR_14": 1.2, "RelativeVolume_5": 2.0})
        
        assert c.inputs["state"] == "HIGH_VOLATILITY"
        assert c.inputs["atr_expanding"] is True

    def test_low_volatility(self):
        self.gen.evaluate(self.ts, {"ATR_14": 1.5, "RelativeVolume_5": 1.0})
        self.gen.evaluate(self.ts, {"ATR_14": 1.2, "RelativeVolume_5": 1.0})
        c = self.gen.evaluate(self.ts, {"ATR_14": 1.0, "RelativeVolume_5": 0.5})
        
        assert c.inputs["state"] == "LOW_VOLATILITY"
        assert c.inputs["atr_contracting"] is True

# ---------------------------------------------------------------------------
# Engine Tests
# ---------------------------------------------------------------------------

class TestConceptEngine:
    def test_engine_integration(self):
        reg = ConceptRegistry()
        reg.register(MomentumConceptGenerator)
        reg.register(TrendConceptGenerator)
        
        engine = ConceptEngine(reg)
        ts = datetime(2025, 1, 1, tzinfo=timezone.utc)
        
        # Missing features should result in 0 confidence concepts
        features = {"ROC_5": None, "RSI_14": 50.0, "EMA_20": 100.0, "SMA_20": 100.0}
        concepts = engine.process(ts, features)
        
        assert concepts["MomentumState"].confidence == 0.0
        assert concepts["TrendState"].confidence == 0.2 # No trend
