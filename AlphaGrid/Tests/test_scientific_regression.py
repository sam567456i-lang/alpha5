"""Scientific Regression Tests.

Ensures that the entire research pipeline produces deterministic results
on a Golden Data Fixture and validates the 6-layer architecture constraints.
"""

import unittest
import pandas as pd
import numpy as np
import os
import shutil
import hashlib
from datetime import datetime, timezone, timedelta
from Backend.research.models.experiment import Experiment
from Backend.research.experiments.experiment import ExperimentConfig
from Backend.research.experiments.registry import ResearchRegistry, ExperimentStatus
from Backend.methodology.registry import METHODOLOGY_REGISTRY, MethodologyMetadata
from Shared.enums.methodology_status import MethodologyStatus
from Backend.research.engine.backtest import BacktestEngine
from Backend.research.strategies import register_all_strategies
import uuid


class TestScientificRegression(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Create Golden Data Fixture
        cls.fixture_dir = "tests/fixtures"
        os.makedirs(cls.fixture_dir, exist_ok=True)
        cls.golden_path = os.path.join(cls.fixture_dir, "golden.parquet")
        
        dates = [datetime(2025, 1, 1, tzinfo=timezone.utc) + timedelta(hours=i) for i in range(100)]
        np.random.seed(42)
        prices = 100.0 + np.cumsum(np.random.normal(0, 1, 100))
        
        df = pd.DataFrame({
            "timestamp": dates,
            "open": prices,
            "high": prices + 0.5,
            "low": prices - 0.5,
            "close": prices,
            "volume": np.random.uniform(100, 1000, 100)
        })
        df.to_parquet(cls.golden_path, engine="pyarrow")
        
        # Calculate Snapshot ID
        def _format_float(val: float) -> str:
            return f"{val:.8f}"
            
        formatted_rows = []
        for _, row in df.iterrows():
            formatted_ts = row["timestamp"].strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            formatted_rows.append([
                formatted_ts,
                _format_float(row["open"]),
                _format_float(row["high"]),
                _format_float(row["low"]),
                _format_float(row["close"]),
                _format_float(row["volume"])
            ])
            
        import json
        canonical_json = json.dumps(formatted_rows, sort_keys=True, separators=(",", ":"))
        import unicodedata
        canonical_json = unicodedata.normalize("NFC", canonical_json)
        cls.snapshot_id = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

        from Backend.research.strategies.registry import StrategyRegistry
        from Backend.research.strategies.definitions import RSI_REVERSION, SUPERTREND_CROSS
        StrategyRegistry.clear()
        StrategyRegistry.register(RSI_REVERSION)
        StrategyRegistry.register(SUPERTREND_CROSS)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.fixture_dir):
            shutil.rmtree(cls.fixture_dir)

    def test_trend_following_determinism(self):
        """Ensures Trend Following produces deterministic states."""
        exp = Experiment(
            id=uuid.uuid4(),
            project_id=uuid.uuid4(),
            dataset_snapshot_id=self.snapshot_id,
            timeframe="1H",
            strategy_id="STRAT-ST-001",
            parameters={"confidence_threshold": 0.5, "cooldown_bars": 3},
            random_seed=42,
            git_hash="a"*40,
            environment_fingerprint="b"*64,
            is_exploratory=True,
            is_archived=False
        )
        
        engine = BacktestEngine()
        result1 = engine.execute(exp, self.golden_path)
        
        engine2 = BacktestEngine()
        result2 = engine2.execute(exp, self.golden_path)
        
        self.assertEqual(result1, result2, "BacktestEngine output must be perfectly deterministic")

    def test_mean_reversion_determinism(self):
        """Ensures Mean Reversion produces deterministic states."""
        exp = Experiment(
            id=uuid.uuid4(),
            project_id=uuid.uuid4(),
            dataset_snapshot_id=self.snapshot_id,
            timeframe="1H",
            strategy_id="STRAT-RSI-001",
            parameters={"confidence_threshold": 0.5, "cooldown_bars": 3},
            random_seed=42,
            git_hash="a"*40,
            environment_fingerprint="b"*64,
            is_exploratory=True,
            is_archived=False
        )
        
        engine = BacktestEngine()
        result1 = engine.execute(exp, self.golden_path)
        
        engine2 = BacktestEngine()
        result2 = engine2.execute(exp, self.golden_path)
        
    def test_research_registry_enforces_rh_prefix(self):
        """Ensures the Research Registry strictly maps RH to EXP."""
        registry = ResearchRegistry()
        with self.assertRaisesRegex(ValueError, "hypothesis_id must start with 'RH_'"):
            registry.log_experiment("INVALID", "EXP_123", {}, ExperimentStatus.COMPLETED, {})
            
        with self.assertRaisesRegex(ValueError, "experiment_id must start with 'EXP_'"):
            registry.log_experiment("RH_123", "INVALID", {}, ExperimentStatus.COMPLETED, {})
            
        registry.log_experiment("RH_123", "EXP_123", {}, ExperimentStatus.COMPLETED, {"sharpe": 1.5})
        record = registry.get_record("EXP_123")
        self.assertEqual(record["hypothesis_id"], "RH_123")

    def test_methodology_registry_metadata(self):
        """Ensures MethodologyRegistry stores rich metadata correctly."""
        meta = MethodologyMetadata(
            name="TestMeta",
            status=MethodologyStatus.VALIDATED,
            version="1.5.0",
            uses_concepts=["TrendState"],
            compatible_features=["SMA"],
            compatible_strategies=["TrendFollowingStrategy"],
            supported_models=["XGBoost"],
            performance_summary={"avg_sharpe": 2.1}
        )
        METHODOLOGY_REGISTRY.register(meta)
        retrieved = METHODOLOGY_REGISTRY.get_metadata("TestMeta")
        self.assertEqual(retrieved.version, "1.5.0")
        self.assertEqual(retrieved.supported_models, ["XGBoost"])

    def test_experiment_config_metadata(self):
        """Ensures ExperimentConfig has the required components."""
        config = ExperimentConfig(
            id="EXP_TEST_001",
            dataset="hash_123",
            timeframe="1H",
            cost_model={"type": "fixed", "value": 0.001},
            slippage_model={"type": "fixed", "bps": 5},
            walkforward_config={"min_training_period": 30, "min_testing_period": 7, "step_size": 7},
            mc_config={"n_simulations": 100},
            strategy_config={"name": "TREND_FOLLOWING"},
            provider_config={"type": "rule"},
            seed=42
        )
        self.assertEqual(config.id, "EXP_TEST_001")


if __name__ == '__main__':
    unittest.main()
