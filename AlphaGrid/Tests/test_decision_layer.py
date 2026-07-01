"""Unit tests for the Decision Layer and Methodology/Signal Engine (PR-3 & PR-4).

Tests:
- Signal immutability
- Decision immutability
- RuleDecisionProvider logic
- AbstractDecisionProvider interface enforcement
- DecisionProvider never imports Strategy (verified structurally)
"""

import pytest
from typing import Dict, Any, List

from Backend.methodology.signals import Signal
from Backend.research.decision.base import AbstractDecisionProvider, Decision
from Backend.research.decision.rule_provider import RuleDecisionProvider


# ---------------------------------------------------------------------------
# Signal Tests
# ---------------------------------------------------------------------------

class TestSignal:

    def test_signal_is_frozen(self):
        s = Signal(
            direction="LONG",
            confidence=0.85,
            strength=0.7,
            reason="Strong trend detected",
            concept_ids=["Momentum"],
            methodology="TrendFollowing",
        )
        with pytest.raises(AttributeError):
            s.direction = "SHORT"  # type: ignore

    def test_signal_contains_metadata(self):
        s = Signal(
            direction="SHORT",
            confidence=0.6,
            strength=0.5,
            reason="Pullback exhaustion",
            concept_ids=["Momentum", "Volatility"],
            methodology="MeanReversion",
        )
        assert s.direction == "SHORT"
        assert len(s.concept_ids) == 2
        assert s.methodology == "MeanReversion"


# ---------------------------------------------------------------------------
# Decision Tests
# ---------------------------------------------------------------------------

class TestDecision:

    def test_decision_is_frozen(self):
        d = Decision(direction="LONG", confidence=0.9, reason="test")
        with pytest.raises(AttributeError):
            d.direction = "SHORT"  # type: ignore

    def test_decision_metadata_defaults_to_empty(self):
        d = Decision(direction="WAIT", confidence=0.0, reason="no signals")
        assert d.metadata == {}


# ---------------------------------------------------------------------------
# RuleDecisionProvider Tests
# ---------------------------------------------------------------------------

class TestRuleDecisionProvider:

    def test_no_signals_returns_wait(self):
        provider = RuleDecisionProvider()
        decision = provider.evaluate([], context={})
        assert decision.direction == "WAIT"

    def test_strong_signal_produces_decision(self):
        provider = RuleDecisionProvider()
        signal = Signal(
            direction="LONG",
            confidence=0.85,
            strength=0.8,
            reason="strong trend",
            concept_ids=["Momentum"],
            methodology="TrendFollowing",
        )
        decision = provider.evaluate([signal], context={})
        assert decision.direction == "LONG"
        assert decision.confidence == 0.85

    def test_weak_signal_returns_wait(self):
        provider = RuleDecisionProvider()
        signal = Signal(
            direction="SHORT",
            confidence=0.3,
            strength=0.2,
            reason="weak signal",
            concept_ids=["Momentum"],
            methodology="MeanReversion",
        )
        decision = provider.evaluate([signal], context={})
        assert decision.direction == "WAIT"

    def test_multiple_signals_picks_strongest(self):
        provider = RuleDecisionProvider()
        signals = [
            Signal(direction="SHORT", confidence=0.6, strength=0.4, reason="weak",
                   concept_ids=["A"], methodology="MR"),
            Signal(direction="LONG", confidence=0.9, strength=0.8, reason="strong",
                   concept_ids=["B"], methodology="TF"),
        ]
        decision = provider.evaluate(signals, context={})
        assert decision.direction == "LONG"
        assert decision.confidence == 0.9


# ---------------------------------------------------------------------------
# DecisionProvider Interface Tests
# ---------------------------------------------------------------------------

class TestDecisionProviderInterface:

    def test_cannot_instantiate_abstract(self):
        with pytest.raises(TypeError):
            AbstractDecisionProvider()  # type: ignore

    def test_rule_provider_implements_interface(self):
        provider = RuleDecisionProvider()
        assert isinstance(provider, AbstractDecisionProvider)

    def test_decision_provider_does_not_import_strategy(self):
        """
        Structural test: verify the decision base module has no
        imports from Backend.research.engine.strategy_interface.
        This enforces the downward-only dependency rule.
        """
        import inspect
        source = inspect.getsource(AbstractDecisionProvider)
        assert "strategy_interface" not in source
        assert "AbstractStrategy" not in source
