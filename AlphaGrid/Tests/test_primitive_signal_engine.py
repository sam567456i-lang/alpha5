from datetime import datetime, timezone

from Backend.signals.primitive.engine import PrimitiveSignalEngine
from Backend.signals.primitive.generators.trend import StrongTrendSignalGenerator
from Backend.signals.primitive.generators.extremum import OverextendedSignalGenerator
from Backend.concepts.base import Concept
from Shared.enums.concept_type import ConceptType
from Shared.enums.concept_state import TrendState, VolatilityState, ExtremumState, StrengthState

def _make_concept(c_id: str, c_type: ConceptType, state: str, conf: float, generator: str) -> Concept:
    return Concept(
        id=c_id,
        type=c_type,
        version="v1",
        timestamp=datetime(2025, 1, 1, tzinfo=timezone.utc),
        confidence=conf,
        inputs={"state": state},
        generator=generator
    )

class TestPrimitiveSignalEngine:
    def setup_method(self):
        self.ts = datetime(2025, 1, 1, tzinfo=timezone.utc)

    def test_strong_trend_positive(self):
        engine = PrimitiveSignalEngine([StrongTrendSignalGenerator()])
        concepts = {
            "TrendState": _make_concept("TrendState", ConceptType.TREND, TrendState.BULLISH, 0.8, "TrendConceptGenerator"),
            "TrendStrength": _make_concept("TrendStrength", ConceptType.STRENGTH, StrengthState.STRONG, 0.7, "StrengthConceptGenerator")
        }
        signals = engine.process(self.ts, list(concepts.values()))
        assert len(signals) == 1
        assert signals[0].id == "STRONG_TREND"
        assert signals[0].direction == 1

    def test_strong_trend_weak_strength(self):
        engine = PrimitiveSignalEngine([StrongTrendSignalGenerator()])
        concepts = {
            "TrendState": _make_concept("TrendState", ConceptType.TREND, TrendState.BULLISH, 0.8, "TrendConceptGenerator"),
            # Weak strength -> No signal
            "TrendStrength": _make_concept("TrendStrength", ConceptType.STRENGTH, StrengthState.WEAK, 0.3, "StrengthConceptGenerator")
        }
        signals = engine.process(self.ts, list(concepts.values()))
        assert len(signals) == 0

    def test_overextended_expanding_volatility(self):
        engine = PrimitiveSignalEngine([OverextendedSignalGenerator()])
        concepts = {
            "ExtremumState": _make_concept("ExtremumState", ConceptType.EXTREMUM, ExtremumState.OVEREXTENDED_BULLISH, 0.9, "ExtremumConceptGenerator"),
            # Expanding volatility invalidates mean reversion
            "VolatilityState": _make_concept("VolatilityState", ConceptType.VOLATILITY, VolatilityState.EXPANDING, 0.8, "VolatilityConceptGenerator")
        }
        signals = engine.process(self.ts, list(concepts.values()))
        assert len(signals) == 0

    def test_overextended_contracting_volatility(self):
        engine = PrimitiveSignalEngine([OverextendedSignalGenerator()])
        concepts = {
            "ExtremumState": _make_concept("ExtremumState", ConceptType.EXTREMUM, ExtremumState.OVEREXTENDED_BEARISH, 0.9, "ExtremumConceptGenerator"),
            # Contracting volatility allows mean reversion
            "VolatilityState": _make_concept("VolatilityState", ConceptType.VOLATILITY, VolatilityState.CONTRACTING, 0.8, "VolatilityConceptGenerator")
        }
        signals = engine.process(self.ts, list(concepts.values()))
        assert len(signals) == 1
        assert signals[0].id == "OVEREXTENDED"
        assert signals[0].direction == 1
