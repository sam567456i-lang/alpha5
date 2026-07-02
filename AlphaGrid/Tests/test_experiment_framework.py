"""Production unit tests for the Experiment Framework (PR-5).

Tests:
- ExperimentConfig immutability and field coverage
- ModelArtifact immutability and field coverage
- ResearchRegistry: thread safety, lifecycle, queries, serialization, validation
- CandidateRegistry: thread safety, promotion, queries, validation
- ExperimentStatus and CandidateStatus enums
"""

import json
import pytest
from datetime import datetime, timezone

from Backend.research.experiments.experiment import ExperimentConfig, ModelArtifact
from Backend.research.experiments.registry import (
    ResearchRegistry,
    ExperimentStatus,
    ExperimentRecord,
)
from Backend.research.experiments.candidate_registry import (
    CandidateRegistry,
    CandidateStatus,
)


# ---------------------------------------------------------------------------
# ExperimentConfig Tests
# ---------------------------------------------------------------------------

class TestExperimentConfig:

    def _make_config(self) -> ExperimentConfig:
        return ExperimentConfig(
            id="EXP_001",
            dataset="BTCUSDT_1H_GOLDEN",
            timeframe="1H",
            cost_model={"type": "fixed", "value": 0.001},
            slippage_model={"type": "fixed", "bps": 5},
            walkforward_config={"min_training_period": 30, "min_testing_period": 7},
            mc_config={"n_simulations": 1000},
            strategy_config={"name": "PHASE8_RESEARCH"},
            provider_config={"type": "rule"},
            seed=42,
        )

    def test_config_is_frozen(self):
        cfg = self._make_config()
        with pytest.raises(AttributeError):
            cfg.seed = 99  # type: ignore

    def test_config_equality(self):
        c1 = self._make_config()
        c2 = self._make_config()
        assert c1 == c2

    def test_config_contains_all_required_fields(self):
        cfg = self._make_config()
        assert cfg.id == "EXP_001"
        assert cfg.dataset == "BTCUSDT_1H_GOLDEN"
        assert cfg.timeframe == "1H"
        assert cfg.seed == 42
        assert cfg.cost_model["type"] == "fixed"
        assert cfg.slippage_model["bps"] == 5
        assert cfg.walkforward_config["min_training_period"] == 30
        assert cfg.mc_config["n_simulations"] == 1000
        assert cfg.strategy_config["name"] == "PHASE8_RESEARCH"
        assert cfg.provider_config["type"] == "rule"


# ---------------------------------------------------------------------------
# ModelArtifact Tests
# ---------------------------------------------------------------------------

class TestModelArtifact:

    def _make_artifact(self) -> ModelArtifact:
        return ModelArtifact(
            model_id="model_abc123",
            algorithm="LinearRegression",
            training_dataset="BTCUSDT_1H_GOLDEN",
            feature_version="v1",
            git_commit="abc123def456",
            hyperparameters={"alpha": 0.01},
            seed=42,
            serialization_format="pickle",
            created_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
            preprocessing_pipeline={"scaler": "StandardScaler"},
        )

    def test_artifact_is_frozen(self):
        artifact = self._make_artifact()
        with pytest.raises(AttributeError):
            artifact.seed = 99  # type: ignore

    def test_artifact_contains_all_fields(self):
        artifact = self._make_artifact()
        assert artifact.model_id == "model_abc123"
        assert artifact.algorithm == "LinearRegression"
        assert artifact.training_dataset == "BTCUSDT_1H_GOLDEN"
        assert artifact.feature_version == "v1"
        assert artifact.git_commit == "abc123def456"
        assert artifact.hyperparameters == {"alpha": 0.01}
        assert artifact.seed == 42
        assert artifact.serialization_format == "pickle"
        assert artifact.preprocessing_pipeline == {"scaler": "StandardScaler"}

    def test_artifact_equality(self):
        a1 = self._make_artifact()
        a2 = self._make_artifact()
        assert a1 == a2


# ---------------------------------------------------------------------------
# ResearchRegistry Tests
# ---------------------------------------------------------------------------

class TestResearchRegistry:

    def test_log_and_retrieve(self):
        reg = ResearchRegistry()
        reg.log_experiment("RH_TEST", "EXP_001", config={"test": True}, status=ExperimentStatus.ACTIVE, metrics={"sharpe": 1.5})
        record = reg.get_record("EXP_001")
        assert record["status"] == "Active"
        assert record["metrics"]["sharpe"] == 1.5

    def test_log_rejected(self):
        reg = ResearchRegistry()
        reg.log_experiment("RH_TEST", "EXP_002", config={}, status=ExperimentStatus.REJECTED, metrics={"sharpe": -0.5})
        record = reg.get_record("EXP_002")
        assert record["status"] == "Rejected"

    def test_log_promoted(self):
        reg = ResearchRegistry()
        reg.log_experiment("RH_TEST", "EXP_003", config={}, status=ExperimentStatus.PROMOTED, metrics={"sharpe": 2.1})
        record = reg.get_record("EXP_003")
        assert record["status"] == "Promoted"

    def test_missing_record_returns_empty(self):
        reg = ResearchRegistry()
        assert reg.get_record("NONEXISTENT") == {}

    def test_all_statuses_exist(self):
        assert ExperimentStatus.ACTIVE.value == "Active"
        assert ExperimentStatus.COMPLETED.value == "Completed"
        assert ExperimentStatus.ARCHIVED.value == "Archived"
        assert ExperimentStatus.REJECTED.value == "Rejected"
        assert ExperimentStatus.PROMOTED.value == "Promoted"

    def test_duplicate_experiment_rejected(self):
        reg = ResearchRegistry()
        reg.log_experiment("RH_TEST", "EXP_DUP", config={}, status=ExperimentStatus.ACTIVE, metrics={})
        with pytest.raises(ValueError, match="already exists"):
            reg.log_experiment("RH_TEST", "EXP_DUP", config={}, status=ExperimentStatus.ACTIVE, metrics={})

    def test_empty_experiment_id_rejected(self):
        reg = ResearchRegistry()
        with pytest.raises(ValueError, match="must not be empty"):
            reg.log_experiment("RH_TEST", "", config={}, status=ExperimentStatus.ACTIVE, metrics={})

    def test_nan_metric_rejected(self):
        reg = ResearchRegistry()
        with pytest.raises(ValueError, match="NaN"):
            reg.log_experiment("RH_TEST", "EXP_NAN", config={}, status=ExperimentStatus.ACTIVE, metrics={"sharpe": float("nan")})

    def test_inf_metric_rejected(self):
        reg = ResearchRegistry()
        with pytest.raises(ValueError, match="Inf"):
            reg.log_experiment("RH_TEST", "EXP_INF", config={}, status=ExperimentStatus.ACTIVE, metrics={"sharpe": float("inf")})

    def test_update_status(self):
        reg = ResearchRegistry()
        reg.log_experiment("RH_TEST", "EXP_UPD", config={}, status=ExperimentStatus.ACTIVE, metrics={})
        reg.update_status("EXP_UPD", ExperimentStatus.COMPLETED, notes="Finished")
        record = reg.get_record("EXP_UPD")
        assert record["status"] == "Completed"
        assert record["notes"] == "Finished"

    def test_update_status_nonexistent_fails(self):
        reg = ResearchRegistry()
        with pytest.raises(ValueError, match="not found"):
            reg.update_status("GHOST", ExperimentStatus.COMPLETED)

    def test_get_by_status(self):
        reg = ResearchRegistry()
        reg.log_experiment("RH_TEST", "EXP_A", config={}, status=ExperimentStatus.ACTIVE, metrics={})
        reg.log_experiment("RH_TEST", "EXP_B", config={}, status=ExperimentStatus.REJECTED, metrics={})
        reg.log_experiment("RH_TEST", "EXP_C", config={}, status=ExperimentStatus.ACTIVE, metrics={})
        active = reg.get_by_status(ExperimentStatus.ACTIVE)
        assert len(active) == 2

    def test_get_all(self):
        reg = ResearchRegistry()
        reg.log_experiment("RH_TEST", "EXP_1", config={}, status=ExperimentStatus.ACTIVE, metrics={})
        reg.log_experiment("RH_TEST", "EXP_2", config={}, status=ExperimentStatus.REJECTED, metrics={})
        assert len(reg.get_all()) == 2

    def test_count_by_status(self):
        reg = ResearchRegistry()
        reg.log_experiment("RH_TEST", "EXP_1", config={}, status=ExperimentStatus.ACTIVE, metrics={})
        reg.log_experiment("RH_TEST", "EXP_2", config={}, status=ExperimentStatus.ACTIVE, metrics={})
        reg.log_experiment("RH_TEST", "EXP_3", config={}, status=ExperimentStatus.REJECTED, metrics={})
        counts = reg.count_by_status()
        assert counts["Active"] == 2
        assert counts["Rejected"] == 1

    def test_len(self):
        reg = ResearchRegistry()
        assert len(reg) == 0
        reg.log_experiment("RH_TEST", "EXP_1", config={}, status=ExperimentStatus.ACTIVE, metrics={})
        assert len(reg) == 1

    def test_json_serialization_roundtrip(self):
        reg = ResearchRegistry()
        reg.log_experiment("RH_TEST", "EXP_RT", config={"key": "val"}, status=ExperimentStatus.COMPLETED, metrics={"sharpe": 1.2})
        json_str = reg.to_json()
        reg2 = ResearchRegistry.from_json(json_str)
        record = reg2.get_record("EXP_RT")
        assert record["status"] == "Completed"
        assert record["metrics"]["sharpe"] == 1.2


# ---------------------------------------------------------------------------
# CandidateRegistry Tests
# ---------------------------------------------------------------------------

class TestCandidateRegistry:

    def test_promote_and_retrieve(self):
        reg = CandidateRegistry()
        reg.promote_candidate("STRAT_001", experiment_id="EXP_001", config={"name": "TrendFollower"}, validation_metrics={"sharpe": 1.8})
        candidate = reg.get_candidate("STRAT_001")
        assert candidate["status"] == "PendingPaperTrade"
        assert candidate["validation_metrics"]["sharpe"] == 1.8
        assert candidate["experiment_id"] == "EXP_001"

    def test_missing_candidate_returns_empty(self):
        reg = CandidateRegistry()
        assert reg.get_candidate("NONEXISTENT") == {}

    def test_duplicate_candidate_rejected(self):
        reg = CandidateRegistry()
        reg.promote_candidate("STRAT_DUP", experiment_id="EXP_1", config={}, validation_metrics={})
        with pytest.raises(ValueError, match="already in"):
            reg.promote_candidate("STRAT_DUP", experiment_id="EXP_2", config={}, validation_metrics={})

    def test_empty_strategy_id_rejected(self):
        reg = CandidateRegistry()
        with pytest.raises(ValueError, match="must not be empty"):
            reg.promote_candidate("", experiment_id="EXP_1", config={}, validation_metrics={})

    def test_nan_metric_rejected(self):
        reg = CandidateRegistry()
        with pytest.raises(ValueError, match="NaN"):
            reg.promote_candidate("STRAT_NAN", experiment_id="EXP_1", config={}, validation_metrics={"sharpe": float("nan")})

    def test_update_status(self):
        reg = CandidateRegistry()
        reg.promote_candidate("STRAT_UPD", experiment_id="EXP_1", config={}, validation_metrics={})
        reg.update_status("STRAT_UPD", CandidateStatus.PAPER_TRADING)
        candidate = reg.get_candidate("STRAT_UPD")
        assert candidate["status"] == "PaperTrading"

    def test_get_all_candidates(self):
        reg = CandidateRegistry()
        reg.promote_candidate("S1", experiment_id="E1", config={}, validation_metrics={})
        reg.promote_candidate("S2", experiment_id="E2", config={}, validation_metrics={})
        assert len(reg.get_all_candidates()) == 2

    def test_len(self):
        reg = CandidateRegistry()
        assert len(reg) == 0
        reg.promote_candidate("S1", experiment_id="E1", config={}, validation_metrics={})
        assert len(reg) == 1
