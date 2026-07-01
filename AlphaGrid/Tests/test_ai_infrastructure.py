"""Production unit tests for the AI Infrastructure (PR-6).

Tests:
- ComputeManager determinism (seed setting)
- AbstractAIModel interface enforcement
- Trainer produces ModelArtifact and proper serialization
- Trainer hash verification and validation
- InferenceEngine loads from bytes, verifies hash
- MLDecisionProvider logic and determinism
"""

import hashlib
import os
import pickle
import pytest
from typing import Any, Dict, Tuple

import numpy as np

from Backend.ai.compute_manager import ComputeManager
from Backend.ai.base_model import AbstractAIModel
from Backend.ai.trainer import Trainer
from Backend.ai.inference import InferenceEngine
from Backend.research.decision.ml_provider import MLDecisionProvider
from Backend.research.experiments.experiment import ModelArtifact


# ---------------------------------------------------------------------------
# Stubs
# ---------------------------------------------------------------------------

class StubModel(AbstractAIModel):
    @classmethod
    def get_family(cls) -> str:
        return "Stub"

    def train(self, features: np.ndarray, labels: np.ndarray) -> Dict[str, float]:
        return {"loss": 0.1, "accuracy": 0.9}

    def predict(self, features: np.ndarray) -> Tuple[str, float]:
        # Simple deterministic behavior based on input sum
        val = np.sum(features)
        if val > 10:
            return "LONG", 0.8
        elif val < -10:
            return "SHORT", 0.7
        return "WAIT", 0.0


class FailingStubModel(AbstractAIModel):
    @classmethod
    def get_family(cls) -> str:
        return "Failing"

    def train(self, features: np.ndarray, labels: np.ndarray) -> Dict[str, float]:
        raise ValueError("Intentional training failure")

    def predict(self, features: np.ndarray) -> Tuple[str, float]:
        raise ValueError("Intentional prediction failure")


class NaNStubModel(AbstractAIModel):
    @classmethod
    def get_family(cls) -> str:
        return "NaN_Producing"

    def train(self, features: np.ndarray, labels: np.ndarray) -> Dict[str, float]:
        return {"loss": float("nan")}

    def predict(self, features: np.ndarray) -> Tuple[str, float]:
        return "WAIT", 0.0


# ---------------------------------------------------------------------------
# ComputeManager Tests
# ---------------------------------------------------------------------------

class TestComputeManager:

    def test_deterministic_seeding(self):
        ComputeManager.set_deterministic(seed=123)
        seq1 = np.random.rand(10).tolist()
        ComputeManager.set_deterministic(seed=123)
        seq2 = np.random.rand(10).tolist()
        assert seq1 == seq2

    def test_thread_limits_set(self):
        ComputeManager.set_deterministic(seed=42, num_threads=2)
        assert os.environ["OMP_NUM_THREADS"] == "2"

    def test_get_optimal_device_returns_string(self):
        assert isinstance(ComputeManager.get_optimal_device(), str)


# ---------------------------------------------------------------------------
# Trainer Tests
# ---------------------------------------------------------------------------

class TestTrainer:

    def setup_method(self):
        self.features = np.random.rand(100, 5)
        self.labels = np.random.randint(0, 2, 100)
        self.config = {"seed": 42, "dataset": "test"}

    def test_successful_training_produces_result(self):
        result = Trainer.train_model(StubModel(), self.config, self.features, self.labels)
        
        assert result.metrics["loss"] == 0.1
        assert result.artifact.algorithm == "Stub"
        assert result.artifact.seed == 42
        
        # Verify serialized model
        loaded = pickle.loads(result.model_bytes)
        assert isinstance(loaded, StubModel)

        # Verify hash
        expected_hash = hashlib.sha256(result.model_bytes).hexdigest()
        assert result.model_hash == expected_hash

    def test_nan_metrics_rejected(self):
        with pytest.raises(ValueError, match="NaN"):
            Trainer.train_model(NaNStubModel(), self.config, self.features, self.labels)

    def test_empty_data_rejected(self):
        empty_features = np.array([])
        empty_labels = np.array([])
        with pytest.raises(ValueError, match="empty"):
            Trainer.train_model(StubModel(), self.config, empty_features, empty_labels)

    def test_nan_data_rejected(self):
        nan_features = self.features.copy()
        nan_features[0, 0] = np.nan
        with pytest.raises(ValueError, match="NaN"):
            Trainer.train_model(StubModel(), self.config, nan_features, self.labels)

    def test_training_failure_bubbles_up(self):
        with pytest.raises(RuntimeError, match="Intentional training failure"):
            Trainer.train_model(FailingStubModel(), self.config, self.features, self.labels)


# ---------------------------------------------------------------------------
# InferenceEngine Tests
# ---------------------------------------------------------------------------

class TestInferenceEngine:

    def setup_method(self):
        features = np.random.rand(10, 5)
        labels = np.random.randint(0, 2, 10)
        self.result = Trainer.train_model(StubModel(), {"seed": 1}, features, labels)

    def test_successful_load_and_predict(self):
        engine = InferenceEngine(
            self.result.artifact, self.result.model_bytes, self.result.model_hash
        )
        assert engine.is_loaded
        direction, conf = engine.predict(np.array([[20.0, 0.0]]))
        assert direction == "LONG"
        
    def test_hash_mismatch_rejected(self):
        with pytest.raises(RuntimeError, match="Model integrity check failed"):
            InferenceEngine(self.result.artifact, self.result.model_bytes, "invalid_hash")

    def test_missing_hash_rejected(self):
        with pytest.raises(ValueError, match="expected_hash is required"):
            InferenceEngine(self.result.artifact, self.result.model_bytes, None)

    def test_structural_test_mode(self):
        # Without bytes, runs in wait mode
        engine = InferenceEngine(self.result.artifact)
        assert not engine.is_loaded
        direction, conf = engine.predict(np.array([[20.0, 0.0]]))
        assert direction == "WAIT"
        assert conf == 0.0

    def test_nan_prediction_input_rejected(self):
        engine = InferenceEngine(
            self.result.artifact, self.result.model_bytes, self.result.model_hash
        )
        with pytest.raises(ValueError, match="NaN"):
            engine.predict(np.array([[np.nan, 0.0]]))


# ---------------------------------------------------------------------------
# MLDecisionProvider Tests
# ---------------------------------------------------------------------------

class TestMLDecisionProvider:

    def setup_method(self):
        features = np.random.rand(10, 2)
        labels = np.random.randint(0, 2, 10)
        self.result = Trainer.train_model(StubModel(), {"seed": 1}, features, labels)

    def test_evaluate_success(self):
        provider = MLDecisionProvider(
            self.result.artifact, 
            self.result.model_bytes, 
            self.result.model_hash,
            feature_names=["f1", "f2"]
        )
        # Sum is 15 -> LONG
        context = {"features": {"f1": 10.0, "f2": 5.0}}
        decision = provider.evaluate([], context)
        assert decision.direction == "LONG"

    def test_missing_features_raises_error(self):
        provider = MLDecisionProvider(
            self.result.artifact, 
            self.result.model_bytes, 
            self.result.model_hash,
            feature_names=["f1", "f2"]
        )
        context = {"features": {"f1": 10.0}} # f2 is missing
        # ML Provider catches ValueError and returns WAIT decision in production
        decision = provider.evaluate([], context)
        assert decision.direction == "WAIT"
        assert "ML inference skipped" in decision.reason

    def test_none_features_returns_wait(self):
        provider = MLDecisionProvider(
            self.result.artifact, 
            self.result.model_bytes, 
            self.result.model_hash,
            feature_names=["f1", "f2"]
        )
        context = {"features": {"f1": 10.0, "f2": None}} # Warmup
        decision = provider.evaluate([], context)
        assert decision.direction == "WAIT"
