"""Production unit tests for Methodology Engine (PR-4)."""

import pytest
from datetime import datetime, timezone

from Backend.signals.primitive.base import PrimitiveSignal
from Backend.signals.primitive.context import SignalContext
from Backend.methodology.trend_following import TrendFollowingMethodology
from Backend.methodology.mean_reversion import MeanReversionMethodology
from Backend.methodology.engine import MethodologyEngine

def _make_signal(id_str: str, direction: int, conf: float = 1.0, signal_type: str = "GENERIC") -> PrimitiveSignal:
    return PrimitiveSignal(
        id=id_str,
        timestamp=datetime(2025, 1, 1, tzinfo=timezone.utc),
        direction=direction,
        confidence=conf,
        signal_type=signal_type,
        supporting_concepts=(),
        generator="Test"
    )

class TestTrendFollowingMethodology:
    def setup_method(self):
        self.methodology = TrendFollowingMethodology()

    def test_long_signal(self):
        signals = (
            _make_signal("STRONG_TREND", direction=1, signal_type="TREND_LONG"),
            _make_signal("DIRECTIONAL_MOMENTUM", direction=0)
        )
        context = SignalContext(signals)
        signal = self.methodology.evaluate(context)
        assert signal.direction == 1
        assert signal.methodology_id == "TrendFollowingMethodology"

    def test_short_signal(self):
        signals = (
            _make_signal("STRONG_TREND", direction=-1, signal_type="TREND_SHORT"),
            _make_signal("DIRECTIONAL_MOMENTUM", direction=0)
        )
        context = SignalContext(signals)
        signal = self.methodology.evaluate(context)
        assert signal.direction == -1

    def test_momentum_blocks_long(self):
        signals = (
            _make_signal("STRONG_TREND", direction=1, signal_type="TREND_LONG"),
            _make_signal("DIRECTIONAL_MOMENTUM", direction=-1, signal_type="MOMENTUM_SHORT")
        )
        context = SignalContext(signals)
        signal = self.methodology.evaluate(context)
        assert signal.is_active == False  # Wait, since momentum contradicts trend

class TestMeanReversionMethodology:
    def setup_method(self):
        self.methodology = MeanReversionMethodology()

    def test_long_signal(self):
        signals = (
            _make_signal("OVEREXTENDED", direction=-1),
        )
        context = SignalContext(signals)
        signal = self.methodology.evaluate(context)
        assert signal.direction == 1

class TestMethodologyEngine:
    def test_engine_integration(self):
        engine = MethodologyEngine([TrendFollowingMethodology(), MeanReversionMethodology()])
        
        signals = (
            _make_signal("STRONG_TREND", direction=1, conf=0.8, signal_type="TREND_LONG"),
        )
        context = SignalContext(signals)
        
        evals = engine.evaluate(context)
        
        # TrendFollowing should fire LONG, MeanReversion should WAIT
        assert len(evals) == 1
        assert evals[0].direction == 1
        assert evals[0].methodology_id == "TrendFollowingMethodology"
