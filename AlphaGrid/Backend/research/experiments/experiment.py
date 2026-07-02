"""Experiment Configuration and Artifacts."""

from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime


@dataclass(frozen=True)
class ExperimentConfig:
    """
    Immutable object locking all parameters required to perfectly
    reproduce an experiment.
    """
    id: str
    dataset: str
    timeframe: str
    cost_model: Dict[str, Any]
    slippage_model: Dict[str, Any]
    walkforward_config: Dict[str, Any]
    mc_config: Dict[str, Any]
    strategy_config: Dict[str, Any]
    provider_config: Dict[str, Any]
    seed: int


@dataclass(frozen=True)
class ModelArtifact:
    """
    Freezes a trained ML model so it can be loaded deterministically
    by the ML Provider during inference.
    """
    model_id: str
    algorithm: str
    training_dataset: str
    feature_version: str
    git_commit: str
    hyperparameters: Dict[str, Any]
    seed: int
    serialization_format: str
    created_at: datetime
    preprocessing_pipeline: Dict[str, Any]
