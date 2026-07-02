"""ML-based Decision Provider.

Evaluates market context using a frozen ML ModelArtifact loaded by
the InferenceEngine. The provider is completely interchangeable with
the RuleDecisionProvider — strategies never know which is active.
"""

import logging
from typing import Any, Dict, List, Optional

import numpy as np

from Backend.methodology.signals import MethodologySignal
from Backend.research.decision.base import AbstractDecisionProvider, Decision
from Backend.research.experiments.experiment import ModelArtifact
from Backend.ai.inference import InferenceEngine

logger = logging.getLogger(__name__)


class MLDecisionProvider(AbstractDecisionProvider):
    """
    Evaluates context using a frozen ML ModelArtifact.

    The model must have been trained offline by the Trainer and serialized
    into a bytes buffer. The InferenceEngine verifies model integrity
    and enforces determinism for every prediction.
    """

    def __init__(
        self,
        model_artifact: ModelArtifact,
        model_bytes: Optional[bytes] = None,
        model_hash: Optional[str] = None,
        feature_names: Optional[List[str]] = None,
    ) -> None:
        """
        Args:
            model_artifact: The immutable artifact describing the trained model.
            model_bytes: Serialized model bytes from Trainer.
            model_hash: SHA-256 hash for integrity verification.
            feature_names: Ordered list of feature names the model expects.
                           Used to extract and order features from context.
        """
        self.engine = InferenceEngine(
            artifact=model_artifact,
            model_bytes=model_bytes,
            expected_hash=model_hash,
        )
        self._feature_names = feature_names or []

    def _extract_features(self, context: Dict[str, Any]) -> Any:

        """
        Extracts and orders feature values from the context dict
        into a numpy array matching the model's expected input shape.

        Args:
            context: Must contain a 'features' dict mapping feature names to values.

        Returns:
            1D numpy array of feature values.

        Raises:
            ValueError: If a required feature is missing or is None.
        """
        raw_features = context.get("features", {})

        if not self._feature_names:
            # Fallback: use all features in sorted order for determinism
            sorted_keys = sorted(raw_features.keys())
            values = []
            for key in sorted_keys:
                val = raw_features[key]
                if val is None:
                    raise ValueError(
                        f"Feature '{key}' is None — cannot run ML inference during warmup"
                    )
                values.append(float(val))
            return np.array(values, dtype=np.float64).reshape(1, -1)

        values = []
        for name in self._feature_names:
            if name not in raw_features:
                raise ValueError(f"Required feature '{name}' not found in context")
            val = raw_features[name]
            if val is None:
                raise ValueError(
                    f"Feature '{name}' is None — cannot run ML inference during warmup"
                )
            values.append(float(val))

        return np.array(values, dtype=np.float64).reshape(1, -1)

    def evaluate(self, signals: List[MethodologySignal], context: Dict[str, Any]) -> Decision:
        """
        Evaluates the market context using the loaded ML model.

        The ML provider ignores the signal list (it makes its own prediction).
        Signals are passed through for interface compatibility.

        Args:
            signals: List of Signal objects (ignored by ML provider).
            context: Must contain a 'features' dict with feature values.

        Returns:
            A Decision object with direction, confidence, reason, and metadata.
        """
        if not self.engine.is_loaded:
            return Decision(
                direction="WAIT",
                confidence=0.0,
                reason="ML model not loaded — operating in structural test mode",
                metadata={"model_id": self.engine.artifact.model_id},
            )

        try:
            features = self._extract_features(context)
            direction, confidence = self.engine.predict(features)
        except ValueError as e:
            logger.warning("ML inference skipped: %s", e)
            return Decision(
                direction="WAIT",
                confidence=0.0,
                reason=f"ML inference skipped: {e}",
                metadata={"model_id": self.engine.artifact.model_id},
            )
        except Exception as e:
            logger.error("ML inference failed: %s", e)
            raise RuntimeError(
                f"ML inference failed for model {self.engine.artifact.model_id}"
            ) from e

        return Decision(
            direction=direction,
            confidence=confidence,
            reason=f"ML Provider ({self.engine.artifact.algorithm}) prediction",
            metadata={
                "model_id": self.engine.artifact.model_id,
                "algorithm": self.engine.artifact.algorithm,
            },
        )
