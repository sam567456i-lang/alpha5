"""Tests for the Research Platform Backtest Engine (Slice 2A)."""

import json
import hashlib
from datetime import datetime, timezone
import pytest
from uuid import uuid4
import os
import tempfile
import unicodedata
from typing import Any, List

from Backend.research.engine.strategy_interface import AbstractStrategy, StrategyRegistry
from Backend.research.engine.dataset_loader import DatasetLoader, DatasetIntegrityError
from Backend.research.engine.backtest import BacktestEngine
from Backend.research.models.experiment import Experiment


class MockStrategy(AbstractStrategy):
    def __init__(self, parameters, random_generator):
        super().__init__(parameters, random_generator)
        self.random_samples = []
        self.events_received = []

    def on_market_event(self, event):
        self.events_received.append(event)
        # Use the injected rng to prove deterministic seeding
        self.random_samples.append(self.rng.random())


def test_strategy_registry_validation():
    registry = StrategyRegistry()
    
    # Valid registration
    registry.register("TEST_1", MockStrategy)
    assert registry.get_strategy("TEST_1") == MockStrategy

    # Invalid regex
    with pytest.raises(ValueError, match="Invalid strategy ID"):
        registry.register("test_1", MockStrategy)
        
    # Duplicate
    with pytest.raises(ValueError, match="Duplicate strategy ID"):
        registry.register("TEST_1", MockStrategy)

    # Invalid class
    class BadStrategy:
        pass
    
    with pytest.raises(TypeError, match="must inherit from AbstractStrategy"):
        registry.register("TEST_2", BadStrategy)


class MockDuckDBResult:
    def __init__(self, rows: List[Any]):
        self.rows = rows

    def fetchall(self) -> List[Any]:
        return self.rows


class MockDuckDBConnection:
    def __init__(self, rows=None):
        self.dt1 = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.dt2 = datetime(2026, 1, 2, tzinfo=timezone.utc)
        
        self.rows = rows if rows is not None else [
            (self.dt1, 100.0, 101.0, 99.0, 100.5, 1000.0),
            (self.dt2, 101.0, 102.0, 100.0, 101.5, 1000.0)
        ]
        self.executed_queries = []

    def execute(self, query: str) -> MockDuckDBResult:
        self.executed_queries.append(query)
        return MockDuckDBResult(self.rows)


def _get_expected_hash() -> str:
    """Helper to compute expected canonical hash manually based on ADP."""
    formatted_rows = [
        ["2026-01-01T00:00:00.000000Z", "100.00000000", "101.00000000", "99.00000000", "100.50000000", "1000.00000000"],
        ["2026-01-02T00:00:00.000000Z", "101.00000000", "102.00000000", "100.00000000", "101.50000000", "1000.00000000"]
    ]
    canonical_json = json.dumps(formatted_rows, sort_keys=True, separators=(",", ":"))
    canonical_json = unicodedata.normalize("NFC", canonical_json)
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


def test_dataset_loader_integrity_and_ordering():
    expected_hash = _get_expected_hash()
    mock_conn = MockDuckDBConnection()
    loader = DatasetLoader(duckdb_conn=mock_conn)
    
    events = list(loader.load_and_verify(expected_hash, "dummy.parquet"))
    assert len(events) == 2
    assert events[0]["timestamp"].strftime("%Y-%m-%dT%H:%M:%S.%fZ") == "2026-01-01T00:00:00.000000Z"
    
    # Verify ORDER BY is in the executed query
    assert "ORDER BY timestamp ASC" in mock_conn.executed_queries[0]
    
    # Should fail integrity (hash mismatch)
    with pytest.raises(DatasetIntegrityError):
        list(loader.load_and_verify("bad_hash", "dummy.parquet"))


def test_dataset_loader_corrupted_dataset():
    # Simulate a corrupted dataset that returns a string instead of a float for 'open'
    mock_conn = MockDuckDBConnection(rows=[
        (datetime(2026, 1, 1, tzinfo=timezone.utc), "corrupted_float", 101.0, 99.0, 100.5, 1000.0)
    ])
    loader = DatasetLoader(duckdb_conn=mock_conn)
    
    # float() casting should fail before yielding any events
    with pytest.raises(ValueError):
        list(loader.load_and_verify("any_hash", "dummy.parquet"))


def _run_backtest(seed: int) -> MockStrategy:
    expected_hash = _get_expected_hash()
    
    from Backend.research.engine.strategy_interface import STRATEGY_REGISTRY
    STRATEGY_REGISTRY._registry.clear()
    STRATEGY_REGISTRY.register("MOCK", MockStrategy)
    
    exp = Experiment(
        id=uuid4(),
        project_id=uuid4(),
        strategy_id="MOCK",
        git_hash="abcdef",
        dataset_snapshot_id=expected_hash,
        environment_fingerprint="f" * 64,
        random_seed=seed,
        parameters={},
        is_exploratory=True,
        is_archived=False,
    )
    
    mock_conn = MockDuckDBConnection()
    loader = DatasetLoader(duckdb_conn=mock_conn)
    engine = BacktestEngine(dataset_loader=loader)
    
    # Instead of just returning the result, let's grab the actual strategy instance to verify state.
    # To do this cleanly for a test, we can patch the strategy instantiation or capture it.
    # Since StrategyRegistry creates it, let's fetch it via a class attribute hack for the test.
    
    strategy_instance = []
    original_get = STRATEGY_REGISTRY.get_strategy
    def patched_get(*args, **kwargs):
        cls = original_get(*args, **kwargs)
        def wrapper(*c_args, **c_kwargs):
            inst = cls(*c_args, **c_kwargs)
            strategy_instance.append(inst)
            return inst
        return wrapper
        
    STRATEGY_REGISTRY.get_strategy = patched_get
    
    engine.execute(exp, "dummy.parquet")
    return strategy_instance[0]


def test_backtest_engine_execution():
    strategy = _run_backtest(42)
    assert len(strategy.events_received) == 2


def test_deterministic_replay():
    # Same seed should produce identical results
    strategy1 = _run_backtest(42)
    strategy2 = _run_backtest(42)
    
    assert strategy1.random_samples == strategy2.random_samples
    assert len(strategy1.random_samples) == 2


def test_different_seed_behavior():
    # Different seeds should produce different results
    strategy1 = _run_backtest(42)
    strategy2 = _run_backtest(999)
    
    assert strategy1.random_samples != strategy2.random_samples
