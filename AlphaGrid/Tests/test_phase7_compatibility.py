"""Phase 7 Compatibility and Regression Tests.

CRITICAL: These tests verify that the Phase 8 additions have NOT broken
any frozen Phase 7 components. This is the most important test suite
in the entire Phase 8 implementation.

Tests:
- AbstractStrategy interface is unchanged
- StrategyRegistry still works
- BacktestEngine still accepts existing strategies
- WalkForwardEngine imports resolve
- Phase 7 research models are unchanged
"""

import pytest
from typing import Any, Dict
from datetime import timedelta
import importlib


# ---------------------------------------------------------------------------
# AbstractStrategy Contract Tests
# ---------------------------------------------------------------------------

class TestAbstractStrategyUnchanged:

    def test_abstract_strategy_importable(self):
        from Backend.research.engine.strategy_interface import AbstractStrategy
        assert AbstractStrategy is not None

    def test_strategy_registry_importable(self):
        from Backend.research.engine.strategy_interface import STRATEGY_REGISTRY
        assert STRATEGY_REGISTRY is not None

    def test_abstract_strategy_has_required_methods(self):
        from Backend.research.engine.strategy_interface import AbstractStrategy
        assert hasattr(AbstractStrategy, "get_parameter_schema")
        assert hasattr(AbstractStrategy, "max_label_horizon")
        assert hasattr(AbstractStrategy, "on_market_event")

    def test_max_label_horizon_default_is_zero(self):
        from Backend.research.engine.strategy_interface import AbstractStrategy

        class DummyStrat(AbstractStrategy):
            def on_market_event(self, event: Dict[str, Any]) -> None:
                pass

        assert DummyStrat.max_label_horizon() == timedelta(0)

    def test_strategy_registry_accepts_valid_ids(self):
        from Backend.research.engine.strategy_interface import AbstractStrategy, StrategyRegistry

        class TestStrat(AbstractStrategy):
            def on_market_event(self, event: Dict[str, Any]) -> None:
                pass

        reg = StrategyRegistry()
        reg.register("TEST_COMPAT_STRAT", TestStrat)
        assert reg.get_strategy("TEST_COMPAT_STRAT") is TestStrat

    def test_strategy_registry_rejects_invalid_id(self):
        from Backend.research.engine.strategy_interface import AbstractStrategy, StrategyRegistry

        class TestStrat(AbstractStrategy):
            def on_market_event(self, event: Dict[str, Any]) -> None:
                pass

        reg = StrategyRegistry()
        with pytest.raises(ValueError, match="Invalid strategy ID"):
            reg.register("invalid-lowercase", TestStrat)


# ---------------------------------------------------------------------------
# BacktestEngine Contract Tests
# ---------------------------------------------------------------------------

class TestBacktestEngineUnchanged:

    def test_backtest_engine_importable(self):
        from Backend.research.engine.backtest import BacktestEngine
        assert BacktestEngine is not None

    def test_backtest_engine_has_execute_method(self):
        from Backend.research.engine.backtest import BacktestEngine
        assert hasattr(BacktestEngine, "execute")


# ---------------------------------------------------------------------------
# WalkForwardEngine Contract Tests
# ---------------------------------------------------------------------------

class TestWalkForwardEngineUnchanged:

    def test_walkforward_engine_importable(self):
        from Backend.research.engine.walkforward import WalkForwardEngine
        assert WalkForwardEngine is not None

    def test_walkforward_engine_has_execute_method(self):
        from Backend.research.engine.walkforward import WalkForwardEngine
        assert hasattr(WalkForwardEngine, "execute")


# ---------------------------------------------------------------------------
# Phase 7 Research Models Unchanged
# ---------------------------------------------------------------------------

class TestPhase7ModelsUnchanged:

    def test_experiment_model_importable(self):
        from Backend.research.models.experiment import Experiment
        assert Experiment is not None

    def test_experiment_model_has_required_fields(self):
        from Backend.research.models.experiment import Experiment
        fields = Experiment.model_fields
        assert "id" in fields
        assert "strategy_id" in fields
        assert "random_seed" in fields
        assert "parameters" in fields
        assert "dataset_snapshot_id" in fields

    def test_backtest_result_importable(self):
        from Backend.research.models.result import BacktestResult
        assert BacktestResult is not None


# ---------------------------------------------------------------------------
# Module Import Health (No Circular Dependencies)
# ---------------------------------------------------------------------------

class TestModuleImportHealth:

    def test_features_import(self):
        importlib.import_module("Backend.features")

    def test_concepts_import(self):
        importlib.import_module("Backend.concepts")

    def test_methodology_import(self):
        importlib.import_module("Backend.methodology")

    def test_decision_import(self):
        importlib.import_module("Backend.research.decision")

    def test_experiments_import(self):
        importlib.import_module("Backend.research.experiments")

    def test_ai_import(self):
        importlib.import_module("Backend.ai")

    def test_existing_research_engine_import(self):
        importlib.import_module("Backend.research.engine")

    def test_no_circular_import_between_features_and_strategy(self):
        """Features must not import strategy_interface."""
        import Backend.features.base as fb
        import inspect
        source = inspect.getsource(fb)
        assert "strategy_interface" not in source
