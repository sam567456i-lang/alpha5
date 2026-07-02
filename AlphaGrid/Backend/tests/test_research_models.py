"""Tests for Research Platform models."""

import json
from datetime import datetime, timezone
from uuid import uuid4
import pytest

from Backend.research.models.dataset import DatasetSnapshot
from Backend.research.models.experiment import Experiment
from Backend.research.models.result import BacktestResult


def test_dataset_snapshot_utc_enforcement():
    """Test that DatasetSnapshot enforces UTC timezone."""
    # Should work with timezone-aware UTC datetime
    now_utc = datetime.now(timezone.utc)
    snapshot = DatasetSnapshot(
        snapshot_id="a" * 64,
        canonical_hash="b" * 64,
        provider="MOCK",
        symbol="AAPL",
        timeframe="1h",
        adjustment_mode="none",
        start_date=now_utc,
        end_date=now_utc,
        storage_path="/data/snapshot.parquet",
        row_count=100,
    )
    assert snapshot.timezone == "UTC"
    assert snapshot.start_date.tzinfo == timezone.utc

    # Should convert naive datetime to UTC
    naive_dt = datetime(2023, 1, 1, 12, 0)
    snapshot2 = DatasetSnapshot(
        snapshot_id="c" * 64,
        canonical_hash="d" * 64,
        provider="MOCK",
        symbol="AAPL",
        timeframe="1h",
        adjustment_mode="none",
        start_date=naive_dt,
        end_date=naive_dt,
        storage_path="/data/snapshot2.parquet",
        row_count=100,
    )
    assert snapshot2.start_date.tzinfo == timezone.utc


def test_experiment_parameter_determinism():
    """Test that experiment parameters are validated for deterministic serialization."""
    # This should pass (clean JSON types)
    exp = Experiment(
        id=uuid4(),
        project_id=uuid4(),
        strategy_id="EMA_CROSS",
        git_hash="abcdef",
        dataset_snapshot_id="e" * 64,
        environment_fingerprint="f" * 64,
        random_seed=42,
        parameters={"ema_slow": 50, "ema_fast": 20},
        is_exploratory=True,
        is_archived=False,
    )
    
    # Prove that the dictionary ordering is serialized deterministically using the ADP rule
    str1 = json.dumps({"ema_slow": 50, "ema_fast": 20}, sort_keys=True, separators=(",", ":"))
    str2 = json.dumps({"ema_fast": 20, "ema_slow": 50}, sort_keys=True, separators=(",", ":"))
    assert str1 == str2

    # This should fail (unserializable type like datetime in parameters)
    with pytest.raises(ValueError, match="no custom objects"):
        Experiment(
            id=uuid4(),
            project_id=uuid4(),
            strategy_id="EMA_CROSS",
            git_hash="abcdef",
            dataset_snapshot_id="e" * 64,
            environment_fingerprint="f" * 64,
            random_seed=42,
            parameters={"invalid_type": datetime.now()},
            is_exploratory=True,
            is_archived=False,
        )

    # This should fail (NaN/Infinity)
    with pytest.raises(ValueError, match="no NaN/Inf"):
        Experiment(
            id=uuid4(),
            project_id=uuid4(),
            strategy_id="EMA_CROSS",
            git_hash="abcdef",
            dataset_snapshot_id="e" * 64,
            environment_fingerprint="f" * 64,
            random_seed=42,
            parameters={"invalid_val": float('inf')},
            is_exploratory=True,
            is_archived=False,
        )


def test_backtest_result_equality():
    """Test standard Pydantic equality semantics on BacktestResult."""
    exp_id = uuid4()
    result1 = BacktestResult(
        experiment_id=exp_id,
        total_return=0.15,
        sharpe_ratio=1.2,
        max_drawdown=0.05,
    )
    result2 = BacktestResult(
        experiment_id=exp_id,
        total_return=0.15,
        sharpe_ratio=1.2,
        max_drawdown=0.05,
    )
    assert result1 == result2
    assert result1.model_dump() == result2.model_dump()
