"""Verification suite for Slice 2B: Validators, WalkForward, Monte Carlo, Replay."""

import pytest
from datetime import datetime, timezone
from typing import Any, Dict

from Backend.research.engine.validators import StrategyValidator, WalkForwardValidator, MonteCarloValidator, ValidationError
from Backend.research.engine.strategy_interface import AbstractStrategy, STRATEGY_REGISTRY
from Backend.research.engine.dataset_loader import DatasetLoader
from Backend.research.engine.walkforward import WalkForwardEngine
from Backend.research.engine.monte_carlo import MonteCarloEngine
from Backend.research.engine.replay import ReplayEngine, ReplayState
from Backend.api.services.research_service import ResearchService
from Backend.research.models.experiment import Experiment
from uuid import uuid4

class ValidatedMockStrategy(AbstractStrategy):
    def __init__(self, parameters: Dict[str, Any], random_generator: Any, **kwargs) -> None:
        super().__init__(parameters, random_generator)
    @classmethod
    def get_parameter_schema(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "period": {"type": int, "required": True, "min": 1, "max": 100},
            "threshold": {"type": float, "required": False, "default": 0.5, "min": 0.0, "max": 1.0}
        }
        
    def on_market_event(self, event: Dict[str, Any]) -> None:
        pass

from Backend.research.strategies.definition import StrategyDefinition
from Backend.methodology.base import AbstractMethodology
from Backend.methodology.evaluation import MethodologyEvaluation

class DummyMethodology(AbstractMethodology):
    def __init__(self): pass
    @classmethod
    def get_name(cls): return "Dummy"
    def evaluate(self, ctx): return MethodologyEvaluation("Dummy", datetime.now(timezone.utc), True, 1, 1.0)

from Backend.research.strategies.registry import StrategyRegistry as DefRegistry

@pytest.fixture(autouse=True)
def setup_validated_mock_registry():
    DefRegistry._definitions["VALIDATED_MOCK"] = StrategyDefinition(
        id="VALIDATED_MOCK",
        strategy_class=ValidatedMockStrategy,
        methodology=DummyMethodology,
        features=[],
        concepts=[],
        primitive_signals=[],
        parameters={}
    )
    if "VALIDATED_MOCK" not in STRATEGY_REGISTRY._registry:
        STRATEGY_REGISTRY.register("VALIDATED_MOCK", ValidatedMockStrategy)

class MockFastDatasetLoader(DatasetLoader):
    def __init__(self, rows=None):
        super().__init__("mock_conn")
        self.rows = rows if rows else [
            {"timestamp": datetime(2026, 1, 1, tzinfo=timezone.utc)},
            {"timestamp": datetime(2026, 2, 1, tzinfo=timezone.utc)},
            {"timestamp": datetime(2026, 3, 1, tzinfo=timezone.utc)},
            {"timestamp": datetime(2026, 4, 1, tzinfo=timezone.utc)},
            {"timestamp": datetime(2026, 5, 1, tzinfo=timezone.utc)},
            {"timestamp": datetime(2026, 6, 1, tzinfo=timezone.utc)},
        ]
        
    def load_and_verify(self, snapshot_id, storage_path, start_bound=None, end_bound=None):
        for r in self.rows:
            if start_bound and r["timestamp"] < start_bound:
                continue
            if end_bound and r["timestamp"] >= end_bound:
                break
            yield r

def get_base_experiment():
    return Experiment(
        id=uuid4(),
        project_id=uuid4(),
        strategy_id="VALIDATED_MOCK",
        git_hash="abcdef",
        dataset_snapshot_id="a"*64,
        environment_fingerprint="b"*64,
        random_seed=42,
        parameters={"period": 14, "threshold": 0.5},
        is_exploratory=True,
        is_archived=False
    )

# ===============================================
# VALIDATOR TESTS
# ===============================================

def test_validator_success_path():
    # Should not raise
    StrategyValidator.validate_parameters("VALIDATED_MOCK", {"period": 14, "threshold": 0.5})

def test_validator_missing_required():
    with pytest.raises(ValidationError, match="Missing required parameter"):
        StrategyValidator.validate_parameters("VALIDATED_MOCK", {"threshold": 0.5})

def test_validator_unsupported_param():
    with pytest.raises(ValidationError, match="Unsupported parameter"):
        StrategyValidator.validate_parameters("VALIDATED_MOCK", {"period": 10, "fake": 1})

def test_validator_type_error():
    with pytest.raises(ValidationError, match="Invalid type"):
        StrategyValidator.validate_parameters("VALIDATED_MOCK", {"period": "10"})

def test_validator_bounds_error():
    with pytest.raises(ValidationError, match="is below minimum"):
        StrategyValidator.validate_parameters("VALIDATED_MOCK", {"period": 0})
        
    with pytest.raises(ValidationError, match="is above maximum"):
        StrategyValidator.validate_parameters("VALIDATED_MOCK", {"period": 14, "threshold": 1.5})

def test_walkforward_validator_missing():
    with pytest.raises(ValidationError, match="Missing required walk-forward config key"):
        WalkForwardValidator.validate_config({"min_training_period": 30})

def test_walkforward_validator_invalid_step():
    with pytest.raises(ValidationError, match="step_size cannot be greater than min_training_period"):
        WalkForwardValidator.validate_config({
            "min_training_period": 30,
            "min_testing_period": 10,
            "step_size": 40
        })

def test_montecarlo_validator_invalid_perturbation():
    with pytest.raises(ValidationError, match="Cannot perturb unsupported parameter"):
        MonteCarloValidator.validate_config({
            "num_iterations": 10,
            "perturbations": {"fake": {"type": "gaussian"}}
        }, "VALIDATED_MOCK")

# ===============================================
# WALKFORWARD ENGINE 
# ===============================================

def test_walkforward_leakage_boundaries_expanding():
    loader = MockFastDatasetLoader()
    engine = WalkForwardEngine(dataset_loader=loader)
    
    config = {
        "min_training_period": 30,
        "min_testing_period": 30,
        "step_size": 30,
        "mode": "expanding"
    }
    
    res = engine.execute(get_base_experiment(), "mock", config)
    folds = res["folds"]
    assert len(folds) >= 2
    
    for i in range(1, len(folds)):
        prev = folds[i-1]
        curr = folds[i]
        
        # OOS must never overlap
        assert curr["oos_start"] >= prev["oos_end"]
        # Expanding mode: IS start remains anchored
        assert curr["is_start"] == prev["is_start"]
        assert curr["is_end"] > prev["is_end"]

def test_walkforward_sliding_mode():
    loader = MockFastDatasetLoader()
    engine = WalkForwardEngine(dataset_loader=loader)
    
    config = {
        "min_training_period": 30,
        "min_testing_period": 30,
        "step_size": 30,
        "mode": "sliding"
    }
    
    res = engine.execute(get_base_experiment(), "mock", config)
    folds = res["folds"]
    assert len(folds) >= 2
    
    for i in range(1, len(folds)):
        prev = folds[i-1]
        curr = folds[i]
        
        # Sliding mode: IS window slides forward
        assert curr["is_start"] > prev["is_start"]
        assert curr["is_end"] > prev["is_end"]

def test_walkforward_partial_final_fold():
    loader = MockFastDatasetLoader()
    engine = WalkForwardEngine(dataset_loader=loader)
    
    config = {
        "min_training_period": 90,
        "min_testing_period": 45,
        "step_size": 30,
        "mode": "expanding"
    }
    
    res = engine.execute(get_base_experiment(), "mock", config)
    folds = res["folds"]
    
    # Must not contain partial folds that are smaller than min_testing_period
    for fold in folds:
        oos_start = datetime.fromisoformat(fold["oos_start"])
        oos_end = datetime.fromisoformat(fold["oos_end"])
        assert (oos_end - oos_start).days >= 40

# ===============================================
# MONTE CARLO ENGINE 
# ===============================================

def test_monte_carlo_determinism():
    loader = MockFastDatasetLoader()
    engine = MonteCarloEngine(dataset_loader=loader)
    
    config = {
        "num_iterations": 5,
        "perturbations": {
            "period": {"type": "discrete", "choices": [10, 14, 20]},
            "threshold": {"type": "gaussian", "std": 0.1}
        }
    }
    
    exp1 = get_base_experiment()
    res1 = engine.execute(exp1, "mock", config)
    
    # Rerun identical root seed -> exact same results
    exp2 = get_base_experiment()
    res2 = engine.execute(exp2, "mock", config)
    
    assert res1["iterations"][0]["seed"] == res2["iterations"][0]["seed"]
    assert res1["iterations"][0]["parameters"] == res2["iterations"][0]["parameters"]
    
    # Rerun different root seed -> deterministic difference
    exp3 = get_base_experiment()
    exp3.random_seed = 999
    res3 = engine.execute(exp3, "mock", config)
    
    assert res1["iterations"][0]["seed"] != res3["iterations"][0]["seed"]

def test_monte_carlo_zero_perturbation():
    loader = MockFastDatasetLoader()
    engine = MonteCarloEngine(dataset_loader=loader)
    
    config = {
        "num_iterations": 2,
        "perturbations": {} # Empty perturbation
    }
    
    exp = get_base_experiment()
    res = engine.execute(exp, "mock", config)
    
    assert res["iterations"][0]["parameters"] == exp.parameters
    assert res["iterations"][1]["parameters"] == exp.parameters

# ===============================================
# REPLAY ENGINE
# ===============================================

def test_replay_state_machine_and_seek():
    loader = MockFastDatasetLoader()
    engine = ReplayEngine(dataset_loader=loader)
    
    engine.initialize("mock_hash", "mock_path")
    assert engine.state == ReplayState.READY
    
    # Start and pause
    engine.start(speed_multiplier=1.0)
    assert engine.state == ReplayState.PLAYING
    
    engine.pause()
    assert engine.state == ReplayState.PAUSED
    
    # Invalid Seek (cannot seek non-existent index)
    with pytest.raises(ValueError):
        engine.seek(bar_index=999)
        
    # Seek by timestamp
    engine.seek(timestamp=datetime(2026, 4, 1, tzinfo=timezone.utc))
    assert engine._current_index == 3 
    
    # Single step
    engine.single_step()
    assert engine._current_index == 4
    
    # Run to completion
    for _ in range(10):
        engine.single_step()
        
    assert engine.state == ReplayState.COMPLETED
    
    # Reset
    engine.reset()
    assert engine.state == ReplayState.READY
    assert engine._current_index == 0

# ===============================================
# CRASH RECOVERY
# ===============================================

def test_research_service_crash_recovery():
    # Simulate DB state where experiment was left Pending (app crashed)
    mock_db_state = {
        "exp-123": "Completed",
        "exp-456": "Pending",
        "exp-789": "Pending"
    }
    
    service = ResearchService(initial_state=mock_db_state)
    
    # Upon initialization, service should recover by marking Pending as Failed
    assert service._pending_experiments["exp-123"] == "Completed"
    assert service._pending_experiments["exp-456"] == "Failed (Application Crash Recovery)"
    assert service._pending_experiments["exp-789"] == "Failed (Application Crash Recovery)"
