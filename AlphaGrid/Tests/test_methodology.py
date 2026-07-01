"""Production unit tests for Methodology Engine (PR-4)."""

import pytest
from datetime import datetime, timezone

from Backend.concepts.base import Concept
from Backend.methodology.trend_following import TrendFollowingMethodology
from Backend.methodology.mean_reversion import MeanReversionMethodology
from Backend.methodology.engine import MethodologyEngine


def _make_concept(id_str: str, state: str, conf: float = 1.0) -> Concept:
    return Concept(
        id=id_str,
        version="v1",
        timestamp=datetime(2025, 1, 1, tzinfo=timezone.utc),
        confidence=conf,
        inputs={"state": state},
        generator="Test"
    )

class TestTrendFollowingMethodology:
    def setup_method(self):
        self.methodology = TrendFollowingMethodology()

    def test_long_signal(self):
        concepts = {
            "TrendState": _make_concept("TrendState", "BULLISH_TREND"),
            "MomentumState": _make_concept("MomentumState", "NEUTRAL")
        }
        signal = self.methodology.evaluate(concepts)
        assert signal.direction == "LONG"
        assert signal.methodology == "TrendFollowing"

    def test_short_signal(self):
        concepts = {
            "TrendState": _make_concept("TrendState", "BEARISH_TREND"),
            "MomentumState": _make_concept("MomentumState", "NEUTRAL")
        }
        signal = self.methodology.evaluate(concepts)
        assert signal.direction == "SHORT"

    def test_overbought_blocks_long(self):
        concepts = {
            "TrendState": _make_concept("TrendState", "BULLISH_TREND"),
            "MomentumState": _make_concept("MomentumState", "OVERBOUGHT")
        }
        signal = self.methodology.evaluate(concepts)
        assert signal.direction == "WAIT"

class TestMeanReversionMethodology:
    def setup_method(self):
        self.methodology = MeanReversionMethodology()

    def test_long_signal(self):
        concepts = {
            "MomentumState": _make_concept("MomentumState", "OVERSOLD"),
            "VolatilityState": _make_concept("VolatilityState", "NORMAL_VOLATILITY")
        }
        signal = self.methodology.evaluate(concepts)
        assert signal.direction == "LONG"

    def test_high_volatility_blocks_reversion(self):
        concepts = {
            "MomentumState": _make_concept("MomentumState", "OVERSOLD"),
            "VolatilityState": _make_concept("VolatilityState", "HIGH_VOLATILITY")
        }
        signal = self.methodology.evaluate(concepts)
        assert signal.direction == "WAIT"

class TestMethodologyEngine:
    def test_engine_integration(self):
        engine = MethodologyEngine([TrendFollowingMethodology(), MeanReversionMethodology()])
        
        concepts = {
            "TrendState": _make_concept("TrendState", "BULLISH_TREND", 0.8),
            "MomentumState": _make_concept("MomentumState", "NEUTRAL", 0.5),
            "VolatilityState": _make_concept("VolatilityState", "NORMAL_VOLATILITY", 0.5)
        }
        
        signals = engine.evaluate(concepts)
        
        # TrendFollowing should fire LONG, MeanReversion should WAIT (excluded)
        assert len(signals) == 1
        assert signals[0].direction == "LONG"
        assert signals[0].methodology == "TrendFollowing"
