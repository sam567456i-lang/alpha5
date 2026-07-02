"""Offline Training Orchestrator.

Trains ML models deterministically, serializes them to byte buffers,
computes integrity hashes, and produces immutable ModelArtifacts.
"""

import hashlib
import io
import logging
import pickle
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple

import numpy as np

from Backend.research.experiments.experiment import ModelArtifact
from .base_model import AbstractAIModel
from .compute_manager import ComputeManager

logger = logging.getLogger(__name__)


class TrainingResult:
    """Encapsulates the output of a training run."""

    __slots__ = ("model_bytes", "model_hash", "metrics", "artifact")

    def __init__(
        self,
        model_bytes: bytes,
        model_hash: str,
        metrics: Dict[str, float],
        artifact: ModelArtifact,
    ) -> None:
        self.model_bytes = model_bytes
        self.model_hash = model_hash
        self.metrics = metrics
        self.artifact = artifact


class Trainer:
    """
    Orchestrates offline model training, producing immutable ModelArtifacts
    with deterministic serialization and integrity verification.
    """

    @staticmethod
    def _validate_metrics(metrics: Dict[str, float]) -> None:
        """
        Validates that training metrics contain no NaN or Inf values.

        Raises:
            ValueError: If any metric is NaN or Inf.
        """
        for key, value in metrics.items():
            if not isinstance(value, (int, float)):
                raise TypeError(
                    f"Training metric '{key}' must be numeric, got {type(value).__name__}"
                )
            if isinstance(value, float):
                if value != value:
                    raise ValueError(f"Training metric '{key}' is NaN — model did not converge")
                if value == float("inf") or value == float("-inf"):
                    raise ValueError(f"Training metric '{key}' is Inf — numerical instability detected")

    @staticmethod
    def _serialize_model(model: AbstractAIModel) -> Tuple[bytes, str]:
        """
        Serializes a trained model to a bytes buffer and computes its SHA-256 hash.

        Args:
            model: The trained model instance.

        Returns:
            Tuple of (serialized bytes, SHA-256 hex digest).

        Raises:
            RuntimeError: If serialization fails.
        """
        try:
            buffer = io.BytesIO()
            pickle.dump(model, buffer, protocol=pickle.HIGHEST_PROTOCOL)
            model_bytes = buffer.getvalue()
        except Exception as e:
            raise RuntimeError(f"Failed to serialize model: {e}") from e

        model_hash = hashlib.sha256(model_bytes).hexdigest()
        return model_bytes, model_hash

    @staticmethod
    def _validate_training_data(features: Any, labels: Any) -> None:

        """
        Validates training data before training begins.

        Raises:
            ValueError: If data is empty, contains NaN, or shapes are incompatible.
        """
        if features.size == 0:
            raise ValueError("Training features array is empty")
        if labels.size == 0:
            raise ValueError("Training labels array is empty")
        if features.shape[0] != labels.shape[0]:
            raise ValueError(
                f"Feature rows ({features.shape[0]}) != label rows ({labels.shape[0]})"
            )
        if np.any(np.isnan(features)):
            raise ValueError("Training features contain NaN values")
        if np.any(np.isnan(labels)):
            raise ValueError("Training labels contain NaN values")

    @staticmethod
    def train_model(
        model: AbstractAIModel,
        config: Dict[str, Any],
        features: Any,

        labels: Any,

        preprocessing_pipeline: Optional[Dict[str, Any]] = None,
    ) -> TrainingResult:
        """
        Trains a model deterministically and produces an immutable artifact.

        Args:
            model: An AbstractAIModel instance to train.
            config: Training configuration containing seed, dataset, feature_version,
                    git_commit, and hyperparameters.
            features: 2D numpy array of training features.
            labels: 1D numpy array of target labels.
            preprocessing_pipeline: Optional dict describing the preprocessing steps.

        Returns:
            TrainingResult containing the serialized model, hash, metrics, and artifact.

        Raises:
            ValueError: If training data is invalid or metrics contain NaN/Inf.
            RuntimeError: If training or serialization fails.
        """
        seed = config.get("seed", 42)
        if not isinstance(seed, int):
            raise TypeError(f"Seed must be an integer, got {type(seed).__name__}")

        # 1. Enforce determinism
        ComputeManager.set_deterministic(seed)

        # 2. Validate inputs
        Trainer._validate_training_data(features, labels)

        # 3. Train
        logger.info(
            "Training %s model | seed=%d | samples=%d | features=%d",
            model.get_family(),
            seed,
            features.shape[0],
            features.shape[1] if features.ndim > 1 else 1,
        )

        try:
            metrics = model.train(features, labels)
        except Exception as e:
            raise RuntimeError(
                f"Training failed for {model.get_family()}: {e}"
            ) from e

        # 4. Validate metrics
        Trainer._validate_metrics(metrics)
        logger.info("Training completed. Metrics: %s", metrics)

        # 5. Serialize model
        model_bytes, model_hash = Trainer._serialize_model(model)
        logger.info(
            "Model serialized | size=%d bytes | hash=%s",
            len(model_bytes),
            model_hash[:16],
        )

        # 6. Build immutable artifact
        model_id = f"model_{uuid.uuid4().hex[:12]}"
        artifact = ModelArtifact(
            model_id=model_id,
            algorithm=model.get_family(),
            training_dataset=config.get("dataset", "unknown"),
            feature_version=config.get("feature_version", "v1"),
            git_commit=config.get("git_commit", "unknown"),
            hyperparameters=config.get("hyperparameters", {}),
            seed=seed,
            serialization_format="pickle",
            created_at=datetime.now(timezone.utc),
            preprocessing_pipeline=preprocessing_pipeline or {},
        )

        return TrainingResult(
            model_bytes=model_bytes,
            model_hash=model_hash,
            metrics=metrics,
            artifact=artifact,
        )
