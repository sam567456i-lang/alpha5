"""Feature Engine DAG Execution Tests."""

import unittest
from datetime import datetime, timezone
from Shared.models.market import MarketSnapshot
from Backend.features.engine import FeatureEngine
from Backend.features.registry import FeatureRegistry
from Backend.features.base import AbstractFeature
from Backend.features.keltner import KeltnerChannelFeature
from Backend.features.volatility import ATRFeature

# Dummy features for testing DAG execution
class DummyEMA(AbstractFeature):
    @classmethod
    def get_name(cls): return "EMA_20"
    @classmethod
    def get_version(cls): return "v1"
    @classmethod
    def get_dependencies(cls): return []
    @classmethod
    def warmup_period(cls): return 1
    def compute(self, snapshot, deps):
        return 100.0

class DummyATR(AbstractFeature):
    @classmethod
    def get_name(cls): return "ATR_14"
    @classmethod
    def get_version(cls): return "v1"
    @classmethod
    def get_dependencies(cls): return []
    @classmethod
    def warmup_period(cls): return 1
    def compute(self, snapshot, deps):
        return 5.0

class TestFeatureEngineDAG(unittest.TestCase):
    """
    Validates FeatureEngine DAG execution invariants.
    """

    def setUp(self):
        self.snapshot = MarketSnapshot(
            symbol="BTCUSD", exchange="BINANCE", instrument_type="SPOT",
            last_price=100.0, open=100.0, high=100.0, low=100.0, close=100.0, volume=10,
            timestamp=datetime.now(timezone.utc)
        )

    def test_dependency_resolution_and_caching(self):
        """Ensures dependencies compute before dependents and are cached correctly."""
        registry = FeatureRegistry()
        registry.register(KeltnerChannelFeature)
        registry.register(DummyEMA)
        registry.register(DummyATR)
        
        engine = FeatureEngine(registry)
        
        # Run warmups (Keltner warmup is 20)
        for _ in range(20):
            engine.process(self.snapshot)
        
        # After warmup
        results = engine.process(self.snapshot)
        
        self.assertIn("EMA_20", results)
        self.assertIn("ATR_14", results)
        self.assertIn("Keltner_20_2", results)
        
        # Verify Keltner used the injected results correctly
        keltner = results["Keltner_20_2"]
        self.assertEqual(keltner["ema"], 100.0)
        self.assertEqual(keltner["upper_band"], 110.0) # 100 + 2 * 5
        self.assertEqual(keltner["lower_band"], 90.0)  # 100 - 2 * 5

    def test_missing_dependency_fails_fast(self):
        """Ensures a missing dependency is caught during DAG resolution, not at runtime."""
        registry = FeatureRegistry()
        registry.register(KeltnerChannelFeature)
        # We purposely omit EMA and ATR
        
        with self.assertRaises(ValueError) as context:
            engine = FeatureEngine(registry)
            
        self.assertIn("not registered", str(context.exception))

if __name__ == '__main__':
    unittest.main()
