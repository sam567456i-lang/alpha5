"""Tests for Research Platform memory repositories."""

from datetime import datetime, timezone
from uuid import uuid4
import pytest

from Backend.research.models.dataset import DatasetSnapshot
from Backend.research.models.experiment import Experiment
from Backend.research.models.result import BacktestResult
from Backend.research.repository.memory import MemoryExperimentRepository, MemoryDatasetSnapshotRepository


@pytest.fixture
def experiment_repo():
    return MemoryExperimentRepository()


@pytest.fixture
def snapshot_repo():
    return MemoryDatasetSnapshotRepository()


@pytest.fixture
def sample_snapshot():
    now = datetime.now(timezone.utc)
    return DatasetSnapshot(
        snapshot_id="a" * 64,
        canonical_hash="b" * 64,
        provider="MOCK",
        symbol="AAPL",
        timeframe="1h",
        adjustment_mode="none",
        start_date=now,
        end_date=now,
        storage_path="/data/test.parquet",
        row_count=100,
    )


@pytest.fixture
def sample_experiment():
    return Experiment(
        id=uuid4(),
        project_id=uuid4(),
        strategy_id="EMA_CROSS",
        git_hash="abcdef",
        dataset_snapshot_id="a" * 64,
        environment_fingerprint="c" * 64,
        random_seed=123,
        parameters={"p": 1},
        is_exploratory=True,
        is_archived=False,
    )


def test_snapshot_repository_crud(snapshot_repo, sample_snapshot):
    # Save
    snapshot_repo.save_snapshot(sample_snapshot)
    
    # Retrieve
    retrieved = snapshot_repo.get_snapshot(sample_snapshot.snapshot_id)
    assert retrieved is not None
    assert retrieved.snapshot_id == sample_snapshot.snapshot_id
    
    # Retrieve unknown
    assert snapshot_repo.get_snapshot("unknown") is None


def test_experiment_repository_crud(experiment_repo, sample_experiment):
    # Save
    experiment_repo.save_experiment(sample_experiment)
    
    # Retrieve
    retrieved = experiment_repo.get_experiment(sample_experiment.id)
    assert retrieved is not None
    assert retrieved.id == sample_experiment.id
    
    # List
    all_exps = experiment_repo.list_experiments()
    assert len(all_exps) == 1
    assert all_exps[0].id == sample_experiment.id


def test_experiment_archival_transaction(experiment_repo, sample_experiment):
    # Setup archived experiment
    archived_exp = sample_experiment.model_copy(update={"is_archived": True})
    result = BacktestResult(
        experiment_id=archived_exp.id,
        total_return=0.1,
        sharpe_ratio=1.0,
        max_drawdown=0.02,
    )
    
    # Atomic save
    experiment_repo.archive_experiment_with_result(archived_exp, result)
    
    # Verify both exist
    assert experiment_repo.get_experiment(archived_exp.id).is_archived is True
    assert experiment_repo.get_result(archived_exp.id) == result


def test_experiment_archival_fails_if_not_archived(experiment_repo, sample_experiment):
    # Ensure it fails if we try to archive an exploratory experiment
    assert sample_experiment.is_archived is False
    result = BacktestResult(
        experiment_id=sample_experiment.id,
        total_return=0.1,
        sharpe_ratio=1.0,
        max_drawdown=0.02,
    )
    
    with pytest.raises(ValueError, match="Experiment must be archived"):
        experiment_repo.archive_experiment_with_result(sample_experiment, result)


def test_experiment_archival_fails_on_id_mismatch(experiment_repo, sample_experiment):
    archived_exp = sample_experiment.model_copy(update={"is_archived": True})
    
    # Create result with different experiment ID
    result = BacktestResult(
        experiment_id=uuid4(),
        total_return=0.1,
        sharpe_ratio=1.0,
        max_drawdown=0.02,
    )
    
    with pytest.raises(ValueError, match="Result experiment_id does not match"):
        experiment_repo.archive_experiment_with_result(archived_exp, result)
