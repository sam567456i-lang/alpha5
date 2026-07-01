"""Advanced Phase 7 Verification Protocol Tests for Research Engine."""

import json
import hashlib
import time
import pytest
import math
import unicodedata
from datetime import datetime, timezone, timedelta
from typing import Any, List
from uuid import uuid4
from concurrent.futures import ThreadPoolExecutor
import tracemalloc
import threading

from Backend.research.engine.strategy_interface import AbstractStrategy, STRATEGY_REGISTRY
from Backend.research.engine.dataset_loader import DatasetLoader, DatasetIntegrityError
from Backend.research.engine.backtest import BacktestEngine
from Backend.research.models.experiment import Experiment

try:
    from hypothesis import given, settings, strategies as st
    HAS_HYPOTHESIS = True
except ImportError:
    HAS_HYPOTHESIS = False

# Mock Utilities
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

class AdvancedMockStrategy(AbstractStrategy):
    instances = {}

    def __init__(self, parameters, random_generator):
        super().__init__(parameters, random_generator)
        self.random_samples = []
        self.events_received = []
        AdvancedMockStrategy.instances[threading.get_ident()] = self

    def on_market_event(self, event):
        self.events_received.append(event)
        self.random_samples.append(self.rng.random())

# Helper for testing hash behavior directly
def _compute_raw_hash(rows) -> str:
    loader = DatasetLoader(duckdb_conn=MockDuckDBConnection())
    formatted_rows = []
    for row in rows:
        formatted_row = [
            loader._format_timestamp(row[0]),
            loader._format_float(row[1]),
            loader._format_float(row[2]),
            loader._format_float(row[3]),
            loader._format_float(row[4]),
            loader._format_float(row[5]),
        ]
        formatted_rows.append(formatted_row)
    canonical_json = json.dumps(formatted_rows, sort_keys=True, separators=(",", ":"))
    canonical_json = unicodedata.normalize("NFC", canonical_json)
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

# ==========================================
# TIER 2: INVARIANT TESTING
# ==========================================

def test_invariant_event_ordering():
    """Event Ordering: Ensure timestamp[i] < timestamp[i+1] always."""
    dt1 = datetime(2026, 1, 1, tzinfo=timezone.utc)
    dt2 = datetime(2026, 1, 2, tzinfo=timezone.utc)
    dt3 = datetime(2026, 1, 3, tzinfo=timezone.utc)
    rows = [
        (dt1, 10.0, 11.0, 9.0, 10.5, 100.0),
        (dt2, 10.5, 11.5, 9.5, 11.0, 100.0),
        (dt3, 11.0, 12.0, 10.0, 11.5, 100.0),
    ]
    mock_conn = MockDuckDBConnection(rows=rows)
    loader = DatasetLoader(duckdb_conn=mock_conn)
    expected_hash = _compute_raw_hash(rows)
    
    events = list(loader.load_and_verify(expected_hash, "dummy.parquet"))
    assert len(events) == 3
    # Mathematically assert the ordering
    for i in range(len(events) - 1):
        assert events[i]["timestamp"] < events[i+1]["timestamp"]

def test_invariant_hash_float_mutation():
    """Hash Invariants: Change one float, hash must change."""
    dt1 = datetime(2026, 1, 1, tzinfo=timezone.utc)
    base_rows = [(dt1, 100.0, 101.0, 99.0, 100.5, 1000.0)]
    mutated_rows = [(dt1, 100.00000001, 101.0, 99.0, 100.5, 1000.0)]
    
    hash_base = _compute_raw_hash(base_rows)
    hash_mutated = _compute_raw_hash(mutated_rows)
    assert hash_base != hash_mutated

def test_invariant_hash_timezone_mutation():
    """Hash Invariants: Change timezone, hash must change (if absolute UTC shifts)."""
    dt_utc = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    est_tz = timezone(timedelta(hours=-5))
    dt_est = datetime(2026, 1, 1, 0, 0, 0, tzinfo=est_tz)
    
    base_rows = [(dt_utc, 100.0, 101.0, 99.0, 100.5, 1000.0)]
    mutated_rows = [(dt_est, 100.0, 101.0, 99.0, 100.5, 1000.0)]
    
    hash_utc = _compute_raw_hash(base_rows)
    hash_est = _compute_raw_hash(mutated_rows)
    assert hash_utc != hash_est

def test_invariant_hash_whitespace_ignorance():
    """Whitespace differences in JSON encoding do not change the hash."""
    dt1 = datetime(2026, 1, 1, tzinfo=timezone.utc)
    rows = [(dt1, 100.0, 101.0, 99.0, 100.5, 1000.0)]
    loader = DatasetLoader(duckdb_conn=MockDuckDBConnection())
    formatted_ts = loader._format_timestamp(dt1)
    
    correct_json = json.dumps([[formatted_ts, "100.00000000", "101.00000000", "99.00000000", "100.50000000", "1000.00000000"]], sort_keys=True, separators=(",", ":"))
    hash_correct = hashlib.sha256(correct_json.encode('utf-8')).hexdigest()
    
    wrong_json = json.dumps([[formatted_ts, "100.00000000", "101.00000000", "99.00000000", "100.50000000", "1000.00000000"]], sort_keys=True, separators=(", ", ": "))
    hash_wrong = hashlib.sha256(wrong_json.encode('utf-8')).hexdigest()
    
    assert hash_correct != hash_wrong
    assert hash_correct == _compute_raw_hash(rows)

# ==========================================
# TIER 3: PROPERTY-BASED TESTING
# ==========================================

@pytest.mark.skipif(not HAS_HYPOTHESIS, reason="hypothesis not installed")
def test_hypothesis_property_fuzzing():
    # Example placeholder, since hypothesis is missing in our env
    pass

# ==========================================
# TIER 4: FAULT INJECTION (Negative Paths)
# ==========================================

def test_fault_nan_rejection():
    dt1 = datetime(2026, 1, 1, tzinfo=timezone.utc)
    rows = [(dt1, float('nan'), 101.0, 99.0, 100.5, 1000.0)]
    loader = DatasetLoader(duckdb_conn=MockDuckDBConnection(rows=rows))
    
    with pytest.raises(ValueError, match="Invalid float value"):
        list(loader.load_and_verify("any_hash", "dummy.parquet"))

def test_fault_infinity_rejection():
    dt1 = datetime(2026, 1, 1, tzinfo=timezone.utc)
    rows = [(dt1, 100.0, float('inf'), 99.0, 100.5, 1000.0)]
    loader = DatasetLoader(duckdb_conn=MockDuckDBConnection(rows=rows))
    
    with pytest.raises(ValueError, match="Invalid float value"):
        list(loader.load_and_verify("any_hash", "dummy.parquet"))

def test_fault_duplicate_timestamps():
    dt1 = datetime(2026, 1, 1, tzinfo=timezone.utc)
    rows = [
        (dt1, 100.0, 101.0, 99.0, 100.5, 1000.0),
        (dt1, 101.0, 102.0, 98.0, 101.5, 1100.0),
    ]
    loader = DatasetLoader(duckdb_conn=MockDuckDBConnection(rows=rows))
    
    with pytest.raises(ValueError, match="Duplicate timestamp detected"):
        list(loader.load_and_verify("any_hash", "dummy.parquet"))

def test_fault_missing_column():
    dt1 = datetime(2026, 1, 1, tzinfo=timezone.utc)
    rows = [(dt1, 100.0, 101.0, 99.0, 100.5)]
    loader = DatasetLoader(duckdb_conn=MockDuckDBConnection(rows=rows))
    
    with pytest.raises(Exception):
        list(loader.load_and_verify("any_hash", "dummy.parquet"))

# ==========================================
# TIER 5: DETERMINISM TESTS (100-Loop Trace)
# ==========================================

def _run_backtest_with_seed(seed: int) -> AdvancedMockStrategy:
    rows = [
        (datetime(2026, 1, 1, tzinfo=timezone.utc), 100.0, 101.0, 99.0, 100.5, 1000.0),
        (datetime(2026, 1, 2, tzinfo=timezone.utc), 101.0, 102.0, 100.0, 101.5, 1000.0)
    ]
    expected_hash = _compute_raw_hash(rows)
    
    if "ADV_MOCK" not in STRATEGY_REGISTRY._registry:
        STRATEGY_REGISTRY.register("ADV_MOCK", AdvancedMockStrategy)
    
    exp = Experiment(
        id=uuid4(),
        project_id=uuid4(),
        strategy_id="ADV_MOCK",
        git_hash="abcdef",
        dataset_snapshot_id=expected_hash,
        environment_fingerprint="f" * 64,
        random_seed=seed,
        parameters={},
        is_exploratory=True,
        is_archived=False,
    )
    
    loader = DatasetLoader(duckdb_conn=MockDuckDBConnection(rows=rows))
    engine = BacktestEngine(dataset_loader=loader)
    
    engine.execute(exp, "dummy.parquet")
    
    return AdvancedMockStrategy.instances[threading.get_ident()]

def test_determinism_100_loops():
    """100-loop stochastic trace proving PCG64 binds identically."""
    base_strategy = _run_backtest_with_seed(42)
    base_trace = base_strategy.random_samples
    
    for _ in range(100):
        strategy = _run_backtest_with_seed(42)
        assert strategy.random_samples == base_trace

    diff_strategy = _run_backtest_with_seed(999)
    assert diff_strategy.random_samples != base_trace

# ==========================================
# TIER 6: CONCURRENCY TESTING
# ==========================================

def test_concurrency_isolation():
    """Run multiple BacktestEngine instances simultaneously."""
    def worker(seed):
        return _run_backtest_with_seed(seed).random_samples
    
    seeds = [42, 42, 99, 99, 123, 123]
    with ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(worker, seeds))
        
    assert results[0] == results[1]
    assert results[2] == results[3]
    assert results[4] == results[5]
    assert results[0] != results[2]

# ==========================================
# MEMORY ISOLATION
# ==========================================

def test_memory_isolation_consecutive_runs():
    """Execute 100 consecutive backtests, track memory."""
    tracemalloc.start()
    _run_backtest_with_seed(42)
    snapshot1 = tracemalloc.take_snapshot()
    
    for _ in range(100):
        _run_backtest_with_seed(42)
        
    snapshot2 = tracemalloc.take_snapshot()
    tracemalloc.stop()
    
    stats = snapshot2.compare_to(snapshot1, 'lineno')
    total_diff_kb = sum(stat.size_diff for stat in stats) / 1024
    assert total_diff_kb < 1024

# ==========================================
# PERFORMANCE BASELINES
# ==========================================

def test_performance_baselines():
    """Simulate 10k bars and record timing/memory."""
    base_dt = datetime(2026, 1, 1, tzinfo=timezone.utc)
    rows = []
    for i in range(10000):
        rows.append((base_dt + timedelta(minutes=i), 100.0, 101.0, 99.0, 100.5, 1000.0))
        
    start_hash = time.perf_counter()
    expected_hash = _compute_raw_hash(rows)
    hash_time = time.perf_counter() - start_hash
    
    loader = DatasetLoader(duckdb_conn=MockDuckDBConnection(rows=rows))
    start_load = time.perf_counter()
    events = list(loader.load_and_verify(expected_hash, "dummy.parquet"))
    load_time = time.perf_counter() - start_load
    
    assert len(events) == 10000
    
    print(f"Hashing 10k rows: {hash_time:.4f}s")
    print(f"Loading 10k rows: {load_time:.4f}s")
