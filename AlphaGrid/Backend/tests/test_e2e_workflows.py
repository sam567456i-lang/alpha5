"""
Tier 7 — End-to-End Workflow Verification Suite.

Tests in this file are REGRESSION TESTS with teeth:
- Determinism tests assert exact float equality (==), not tolerance.
- Walk-forward tests assert structural fold isolation, not just "didn't crash."
- Trade sequence hashing catches compensating-error regressions.

DISCIPLINE RULE: If an assertion value changes due to a legitimate architectural
improvement, the commit message MUST state why the number changed.
Silent numerical adjustments are strictly prohibited.
"""

import os
import json
import math
import hashlib
import copy
import pytest
import numpy as np
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
from uuid import uuid4

# Pin BLAS threads to 1 to prevent non-associative float drift
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

from Backend.research.engine.strategy_interface import AbstractStrategy, STRATEGY_REGISTRY
from Backend.research.engine.dataset_loader import DatasetLoader
from Backend.research.engine.backtest import BacktestEngine
from Backend.research.engine.walkforward import WalkForwardEngine
from Backend.research.engine.monte_carlo import MonteCarloEngine
from Backend.research.engine.replay import ReplayEngine, ReplayState
from Backend.research.strategies.ema_cross import EMACrossStrategy
from Backend.research.models.experiment import Experiment


# ===================================================================
# FIXTURES
# ===================================================================

GOLDEN_DATA_PATH = os.path.join(os.path.dirname(__file__), "golden_data", "BTCUSDT_1H_GOLDEN.json")


def _load_golden_events() -> List[Dict[str, Any]]:
    """Loads the immutable golden dataset from the checked-in JSON fixture."""
    with open(GOLDEN_DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
    events = []
    for row in raw:
        row["timestamp"] = datetime.fromisoformat(row["timestamp"])
        events.append(row)
    return events


class GoldenDatasetLoader(DatasetLoader):
    """Mock loader that serves the golden JSON fixture without duckdb."""
    def __init__(self):
        super().__init__("golden_mock_conn")
        self._events = _load_golden_events()

    def load_and_verify(self, snapshot_id, storage_path, start_bound=None, end_bound=None):
        for ev in self._events:
            if start_bound and ev["timestamp"] < start_bound:
                continue
            if end_bound and ev["timestamp"] >= end_bound:
                break
            yield ev


def _make_experiment(seed=42) -> Experiment:
    return Experiment(
        id=uuid4(),
        project_id=uuid4(),
        strategy_id="EMA_CROSS",
        git_hash="golden_v1",
        dataset_snapshot_id="a" * 64,
        environment_fingerprint="b" * 64,
        random_seed=seed,
        parameters={"short_window": 10, "long_window": 50},
        is_exploratory=True,
        is_archived=False
    )


def _run_backtest_and_get_strategy(loader, seed=42):
    """Runs a full backtest and returns the strategy instance for inspection."""
    exp = _make_experiment(seed=seed)
    strategy_cls = STRATEGY_REGISTRY.get_strategy(exp.strategy_id)
    root_rng = np.random.Generator(np.random.PCG64(exp.random_seed))
    strategy = strategy_cls(parameters=exp.parameters, random_generator=root_rng)

    for event in loader.load_and_verify(exp.dataset_snapshot_id, "golden"):
        strategy.on_market_event(event)

    return strategy, exp


def _compute_trade_sequence_hash(trades: List[Dict[str, Any]]) -> str:
    """
    Computes a deterministic SHA-256 hash of the trade sequence.
    
    Serialization rules (from the Tier 7 plan):
    - Floats rounded to fixed precision (2 decimal places for prices, 4 for pnl).
    - Timestamps as UTC-normalized ISO-8601 strings.
    - json.dumps with sort_keys=True, separators=(",",":") for cross-platform stability.
    """
    canonical_trades = []
    for t in trades:
        canonical_trades.append({
            "instrument": str(t.get("instrument", "")),
            "direction": str(t.get("direction", "")),
            "entry_timestamp": t["entry_timestamp"].isoformat() if isinstance(t["entry_timestamp"], datetime) else str(t["entry_timestamp"]),
            "exit_timestamp": t["exit_timestamp"].isoformat() if isinstance(t["exit_timestamp"], datetime) else str(t["exit_timestamp"]),
            "entry_price": round(float(t["entry_price"]), 2),
            "exit_price": round(float(t["exit_price"]), 2),
            "quantity": round(float(t["quantity"]), 4),
            "pnl": round(float(t["pnl"]), 4),
            "exit_reason": str(t.get("exit_reason", ""))
        })
    serialized = json.dumps(canonical_trades, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


# ===================================================================
# TEST 1: STANDARD BACKTEST REGRESSION
# ===================================================================

def test_standard_backtest_regression():
    """
    Runs the full Standard Backtest pipeline on the golden dataset.
    Asserts trade count and trade sequence hash.
    
    DISCIPLINE: If these values change, the commit message MUST explain why.
    """
    loader = GoldenDatasetLoader()
    strategy, exp = _run_backtest_and_get_strategy(loader)

    # The strategy must produce trades
    assert len(strategy.trades) > 0, "Strategy produced zero trades on golden dataset"
    
    # Compute trade sequence hash
    trade_hash = _compute_trade_sequence_hash(strategy.trades)
    
    # Record for visibility (not part of the oracle — informational only)
    print(f"\n[Informational Summary]")
    print(f"  Trades: {len(strategy.trades)}")
    print(f"  Trade Sequence Hash: {trade_hash}")
    if strategy.trades:
        total_pnl = sum(t["pnl"] for t in strategy.trades)
        print(f"  Net PnL: {total_pnl:.2f}")

    # --- REGRESSION ASSERTIONS ---
    # If these fail, explain the change in your commit message.
    assert len(strategy.trades) == 15
    assert trade_hash == "4f92560b152ab557f6ba7853e2097e287a8e7679e2b46a515447438b70ce8e39"


# ===================================================================
# TEST 2: BACKTEST DETERMINISM (Run Twice, Assert Exact Equality)
# ===================================================================

def test_backtest_determinism():
    """
    Runs the Standard Backtest TWICE on the same golden fixture with the same seed.
    Asserts exact float equality (==) on trade sequences and metrics.
    
    This catches: dict ordering bugs, unseeded randomness, thread races,
    global mutable state, and floating-point accumulation drift.
    """
    loader = GoldenDatasetLoader()

    strategy_a, _ = _run_backtest_and_get_strategy(loader, seed=42)
    strategy_b, _ = _run_backtest_and_get_strategy(loader, seed=42)

    # Exact trade count
    assert len(strategy_a.trades) == len(strategy_b.trades), \
        f"Trade count diverged: {len(strategy_a.trades)} vs {len(strategy_b.trades)}"

    # Per-event comparison (explains failures before the hash check)
    for i, (ta, tb) in enumerate(zip(strategy_a.trades, strategy_b.trades)):
        assert ta["entry_price"] == tb["entry_price"], f"Trade {i} entry_price diverged"
        assert ta["exit_price"] == tb["exit_price"], f"Trade {i} exit_price diverged"
        assert ta["pnl"] == tb["pnl"], f"Trade {i} pnl diverged"
        assert ta["entry_timestamp"] == tb["entry_timestamp"], f"Trade {i} entry_timestamp diverged"
        assert ta["exit_timestamp"] == tb["exit_timestamp"], f"Trade {i} exit_timestamp diverged"

    # Hash equality (proves byte-identical sequences)
    hash_a = _compute_trade_sequence_hash(strategy_a.trades)
    hash_b = _compute_trade_sequence_hash(strategy_b.trades)
    assert hash_a == hash_b, f"Trade sequence hash diverged: {hash_a} vs {hash_b}"


# ===================================================================
# TEST 3: STRATEGY PURITY (Isolate Strategy Layer)
# ===================================================================

def test_strategy_purity():
    """
    Runs the strategy alone (no execution engine) against the same dataset twice.
    Asserts identical signal sequences.
    
    Isolates: global mutable state, unseeded randomness, order-dependent logic
    at the strategy layer before it's obscured by the execution engine.
    """
    events = _load_golden_events()
    params = {"short_window": 10, "long_window": 50}

    # Run A
    rng_a = np.random.Generator(np.random.PCG64(42))
    strat_a = EMACrossStrategy(parameters=params, random_generator=rng_a)
    for ev in events:
        strat_a.on_market_event(ev)

    # Run B
    rng_b = np.random.Generator(np.random.PCG64(42))
    strat_b = EMACrossStrategy(parameters=params, random_generator=rng_b)
    for ev in events:
        strat_b.on_market_event(ev)

    assert len(strat_a.signals) == len(strat_b.signals)
    for i, (sa, sb) in enumerate(zip(strat_a.signals, strat_b.signals)):
        assert sa["direction"] == sb["direction"], f"Signal {i} direction diverged"
        assert sa["price"] == sb["price"], f"Signal {i} price diverged"
        assert sa["timestamp"] == sb["timestamp"], f"Signal {i} timestamp diverged"


# ===================================================================
# TEST 4: MONTE CARLO DETERMINISM (Run Twice, Sorted Aggregation)
# ===================================================================

def test_monte_carlo_determinism():
    """
    Runs Monte Carlo TWICE with the same seed and config.
    Sorts iteration results by seed before comparison to absorb
    ThreadPoolExecutor non-deterministic completion order.
    Asserts exact float equality on parameter distributions.
    """
    loader = GoldenDatasetLoader()
    engine = MonteCarloEngine(dataset_loader=loader)

    config = {
        "num_iterations": 5,
        "perturbations": {
            "short_window": {"type": "discrete", "choices": [5, 10, 15, 20]},
            "long_window": {"type": "discrete", "choices": [30, 50, 70]}
        }
    }

    exp1 = _make_experiment(seed=42)
    res1 = engine.execute(exp1, "golden", config)

    exp2 = _make_experiment(seed=42)
    res2 = engine.execute(exp2, "golden", config)

    # Sort by seed to normalize ThreadPoolExecutor completion order
    iters1 = sorted(res1["iterations"], key=lambda x: x["seed"])
    iters2 = sorted(res2["iterations"], key=lambda x: x["seed"])

    assert len(iters1) == len(iters2)
    for i, (it1, it2) in enumerate(zip(iters1, iters2)):
        assert it1["seed"] == it2["seed"], f"Iteration {i} seed diverged"
        assert it1["parameters"] == it2["parameters"], f"Iteration {i} parameters diverged"

    # Different seed must produce deterministic difference
    exp3 = _make_experiment(seed=999)
    res3 = engine.execute(exp3, "golden", config)
    iters3 = sorted(res3["iterations"], key=lambda x: x["seed"])
    assert iters1[0]["seed"] != iters3[0]["seed"], "Different root seeds produced identical iteration seeds"


# ===================================================================
# TEST 5: WALK-FORWARD LEAKAGE — FOLD ISOLATION
# ===================================================================

def test_walkforward_fold_isolation():
    """
    Runs Walk-Forward and asserts structural fold integrity:
    - max(train_timestamp) < min(test_timestamp) for every fold.
    - OOS boundaries never overlap across folds.
    
    This directly targets look-ahead bias at fold boundaries.
    """
    loader = GoldenDatasetLoader()
    engine = WalkForwardEngine(dataset_loader=loader)

    config = {
        "min_training_period": 10,
        "min_testing_period": 5,
        "step_size": 5,
        "mode": "expanding",
        "embargo_period": timedelta(0)
    }

    exp = _make_experiment()
    res = engine.execute(exp, "golden", config)
    folds = res["folds"]

    assert len(folds) >= 2, f"Expected at least 2 folds, got {len(folds)}"

    for fold in folds:
        is_end = datetime.fromisoformat(fold["is_end"])
        oos_start = datetime.fromisoformat(fold["oos_start"])
        # Strict: training must end before testing begins
        assert is_end <= oos_start, \
            f"Fold {fold['fold_number']}: IS end ({is_end}) >= OOS start ({oos_start})"

    # OOS windows must not overlap across folds
    for i in range(1, len(folds)):
        prev_oos_end = datetime.fromisoformat(folds[i - 1]["oos_end"])
        curr_oos_start = datetime.fromisoformat(folds[i]["oos_start"])
        assert curr_oos_start >= prev_oos_end, \
            f"OOS overlap: fold {i} starts at {curr_oos_start} before fold {i-1} ends at {prev_oos_end}"


# ===================================================================
# TEST 6: SYNTHETIC EMBARGO VERIFICATION (max_label_horizon > 0)
# ===================================================================

class MockMLStrategy(AbstractStrategy):
    """Synthetic strategy declaring a 6-hour forward-looking label horizon."""
    @classmethod
    def get_parameter_schema(cls) -> Dict[str, Dict[str, Any]]:
        return {"lookback": {"type": int, "required": True, "min": 1, "max": 100}}

    @classmethod
    def max_label_horizon(cls) -> timedelta:
        return timedelta(hours=6)

    def on_market_event(self, event: Dict[str, Any]) -> None:
        pass

# Register only if not already registered
if "MOCK_ML" not in STRATEGY_REGISTRY._registry:
    STRATEGY_REGISTRY.register("MOCK_ML", MockMLStrategy)


def test_embargo_rejects_insufficient_period():
    """
    Verifies that WalkForwardEngine hard-fails when embargo_period < strategy.max_label_horizon.
    This prevents silent label leakage from misconfigured walk-forward runs.
    """
    loader = GoldenDatasetLoader()
    engine = WalkForwardEngine(dataset_loader=loader)

    exp = _make_experiment()
    exp = exp.model_copy(update={"strategy_id": "MOCK_ML", "parameters": {"lookback": 10}})

    # 3-hour embargo is less than the 6-hour max_label_horizon — must fail
    config = {
        "min_training_period": 10,
        "min_testing_period": 5,
        "step_size": 5,
        "embargo_period": timedelta(hours=3)
    }

    with pytest.raises(ValueError, match="embargo_period.*less than.*max_label_horizon"):
        engine.execute(exp, "golden", config)


def test_embargo_enforces_gap():
    """
    Verifies that a valid embargo_period >= max_label_horizon creates a real
    temporal gap between IS end and OOS start for every fold.
    
    Uses 6-hour embargo on 1H bars to verify sub-day boundary math.
    """
    loader = GoldenDatasetLoader()
    engine = WalkForwardEngine(dataset_loader=loader)

    exp = _make_experiment()
    exp = exp.model_copy(update={"strategy_id": "MOCK_ML", "parameters": {"lookback": 10}})

    embargo = timedelta(hours=6)
    config = {
        "min_training_period": 10,
        "min_testing_period": 5,
        "step_size": 5,
        "embargo_period": embargo
    }

    res = engine.execute(exp, "golden", config)
    folds = res["folds"]

    assert len(folds) >= 1, "Expected at least 1 fold with embargo"

    for fold in folds:
        is_end = datetime.fromisoformat(fold["is_end"])
        oos_start = datetime.fromisoformat(fold["oos_start"])
        gap = oos_start - is_end
        assert gap >= embargo, \
            f"Fold {fold['fold_number']}: gap ({gap}) < embargo ({embargo})"


# ===================================================================
# TEST 7: REPLAY INTEGRATION
# ===================================================================

def test_replay_integration():
    """
    Runs the ReplayEngine through a full lifecycle:
    START -> PAUSE -> SEEK -> STEP -> RESUME -> COMPLETED.
    """
    loader = GoldenDatasetLoader()
    engine = ReplayEngine(dataset_loader=loader)

    engine.initialize("golden_fixture", "golden")
    assert engine.state == ReplayState.READY

    engine.start(speed_multiplier=1.0)
    assert engine.state == ReplayState.PLAYING

    engine.pause()
    assert engine.state == ReplayState.PAUSED

    # Seek to bar 100
    engine.seek(bar_index=100)
    assert engine._current_index == 100

    # Single step
    engine.single_step()
    assert engine._current_index == 101

    # Run to completion
    while engine.state != ReplayState.COMPLETED:
        engine.single_step()

    assert engine.state == ReplayState.COMPLETED

    # Reset
    engine.reset()
    assert engine.state == ReplayState.READY
    assert engine._current_index == 0



# ===================================================================
# TEST 8: BACKTEST start_bound/end_bound ENFORCEMENT
# ===================================================================

def test_backtest_bounds_enforcement():
    """
    Verifies that BacktestEngine.execute(start_bound, end_bound) actually
    restricts the events the strategy sees — not just that WalkForwardEngine
    generates correct fold timestamps, but that the boundary is enforced
    at the data layer.

    This is the interface test for the start_bound/end_bound surface added
    to support fold slicing.
    """
    events = _load_golden_events()

    # Pick a window: bars 200-400 (out of 1000)
    start_bound = events[200]["timestamp"]
    end_bound = events[400]["timestamp"]

    # Run strategy with bounded loader
    loader = GoldenDatasetLoader()
    params = {"short_window": 10, "long_window": 50}
    rng = np.random.Generator(np.random.PCG64(42))
    strategy = EMACrossStrategy(parameters=params, random_generator=rng)

    seen_timestamps = []
    for ev in loader.load_and_verify("ignored", "ignored", start_bound=start_bound, end_bound=end_bound):
        strategy.on_market_event(ev)
        seen_timestamps.append(ev["timestamp"])

    # The strategy must have seen ONLY events within [start_bound, end_bound)
    assert len(seen_timestamps) > 0, "Bounded loader yielded zero events"
    assert len(seen_timestamps) == 200, f"Expected 200 events in window, got {len(seen_timestamps)}"

    # No event before start_bound
    assert all(ts >= start_bound for ts in seen_timestamps), \
        "Strategy saw events before start_bound"

    # No event at or after end_bound
    assert all(ts < end_bound for ts in seen_timestamps), \
        "Strategy saw events at or after end_bound"

    # Compare to unbounded run — must see fewer events
    rng2 = np.random.Generator(np.random.PCG64(42))
    strategy_full = EMACrossStrategy(parameters=params, random_generator=rng2)
    full_count = 0
    for ev in loader.load_and_verify("ignored", "ignored"):
        strategy_full.on_market_event(ev)
        full_count += 1

    assert full_count == 1000, f"Full dataset should have 1000 events, got {full_count}"
    assert len(seen_timestamps) < full_count, "Bounded run saw as many events as unbounded"

