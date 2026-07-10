import unittest
import math
from Backend.core.engines.statistics.distribution_engine import DistributionEngine
from Backend.core.engines.statistics.volatility_engine import VolatilityEngine

class TestStatisticsFamily(unittest.TestCase):
    
    def setUp(self):
        self.dist_engine = DistributionEngine()
        self.vol_engine = VolatilityEngine()

    def test_distribution_engine_basic(self):
        # We need at least 2 events for distribution to emit evidence
        self.dist_engine.process_event({"symbol": "BTC", "close": 100})
        ev = self.dist_engine.process_event({"symbol": "BTC", "close": 110})
        
        self.assertIsNotNone(ev)
        self.assertEqual(ev.mean, 105.0)
        self.assertEqual(ev.variance, 50.0) # ( (100-105)^2 + (110-105)^2 ) / 1 = 50

    def test_volatility_engine_basic(self):
        # TR = max(110-90, 110-100, 90-100) = 20
        ev = self.vol_engine.process_event({"symbol": "BTC", "high": 110, "low": 90, "prev_close": 100})
        self.assertEqual(ev.true_range, 20.0)
        self.assertEqual(ev.atr, 20.0)

    # --- Step 11: Numerical Stability Tests ---
    
    def test_distribution_constant_prices(self):
        self.dist_engine.process_event({"symbol": "BTC", "close": 100})
        ev = self.dist_engine.process_event({"symbol": "BTC", "close": 100})
        self.assertEqual(ev.variance, 0.0)
        self.assertEqual(ev.skewness, 0.0)
        self.assertEqual(ev.kurtosis, 0.0)

    def test_volatility_zero_range(self):
        ev = self.vol_engine.process_event({"symbol": "BTC", "high": 100, "low": 100, "prev_close": 100})
        self.assertEqual(ev.true_range, 0.0)
        self.assertEqual(ev.parkinson_volatility, 0.0)

if __name__ == "__main__":
    unittest.main()
