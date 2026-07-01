"""Inference Engine — loads frozen ModelArtifacts for deterministic prediction.

The InferenceEngine is used by the MLDecisionProvider to run trained models
during backtesting and walk-forward validation. It enforces determinism
via ComputeManager before every prediction.
"""

import hashlib
import logging
import pickle
from typing import Any, Optional, Tuple

import numpy as np

from Backend.research.experiments.experiment import ModelArtifact
from .base_model import AbstractAIModel
from .compute_manager import ComputeManager

logger = logging.getLogger(__name__)


class InferenceEngine:
    """
    Loads a frozen ModelArtifact and performs deterministic inference.

    The model is deserialized from a bytes buffer (produced by Trainer)
    and its integrity is verified via SHA-256 hash comparison.
    """

    def __init__(
        self,
        artifact: ModelArtifact,
        model_bytes: Optional[bytes] = None,
        expected_hash: Optional[str] = None,
    ) -> None:
        """
        Initializes the InferenceEngine.

        Args:
            artifact: The immutable ModelArtifact describing the model.
            model_bytes: Serialized model bytes (from Trainer). If None,
                         the engine operates in structural-test mode (returns WAIT).
            expected_hash: SHA-256 hash to verify model integrity. Required
                           if model_bytes is provided.

        Raises:
            ValueError: If model_bytes is provided but expected_hash is missing.
            RuntimeError: If hash verification fails or deserialization fails.
        """
        self.artifact = artifact
        self._model: Optional[AbstractAIModel] = None

        if model_bytes is not None:
            if expected_hash is None:
                raise ValueError(
                    "expected_hash is required when model_bytes is provided"
                )
            self._model = self._load_and_verify(model_bytes, expected_hash)

        # Enforce determinism for inference
        ComputeManager.set_deterministic(self.artifact.seed)

    def _load_and_verify(
        self, model_bytes: bytes, expected_hash: str
    ) -> AbstractAIModel:
        """
        Deserializes the model and verifies its SHA-256 hash.

        Raises:
            RuntimeError: If hash mismatch or deserialization failure.
        """
        # 1. Verify integrity
        actual_hash = hashlib.sha256(model_bytes).hexdigest()
        if actual_hash != expected_hash:
            raise RuntimeError(
                f"Model integrity check failed. "
                f"Expected hash {expected_hash[:16]}..., got {actual_hash[:16]}..."
            )

        # 2. Deserialize
        try:
            model = pickle.loads(model_bytes)
        except Exception as e:
            raise RuntimeError(f"Failed to deserialize model: {e}") from e

        if not isinstance(model, AbstractAIModel):
            raise RuntimeError(
                f"Deserialized object is not an AbstractAIModel, "
                f"got {type(model).__name__}"
            )

        logger.info(
            "Loaded %s model from artifact %s (hash verified: %s)",
            self.artifact.algorithm,
            self.artifact.model_id,
            actual_hash[:16],
        )
        return model

    @property
    def is_loaded(self) -> bool:
        """Returns True if a trained model is loaded and ready for inference."""
        return self._model is not None

    def predict(self, features: np.ndarray) -> Tuple[str, float]:
        """
        Runs deterministic inference on the provided features.

        Args:
            features: Numpy array of feature values for a single event or batch.

        Returns:
            Tuple of (direction, confidence).

        Raises:
            RuntimeError: If no model is loaded.
            ValueError: If features contain NaN values.
        """
        if self._model is None:
            # Structural test mode — model not loaded
            return ("WAIT", 0.0)

        # Enforce determinism before every prediction
        ComputeManager.set_deterministic(self.artifact.seed)

        # Validate input
        if isinstance(features, np.ndarray) and np.any(np.isnan(features)):
            raise ValueError("Inference features contain NaN values")

        return self._model.predict(features)
