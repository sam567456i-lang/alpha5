import unittest
from Backend.core.interfaces.profile_framework import ProfileIdentity
from Backend.core.interfaces.market_data import Bar, TemporalContext
from Backend.core.analytical_rules.market_profile_rules import TPOAccumulator, TPOProfileEngine

class TestProfileFramework(unittest.TestCase):
    def setUp(self):
        self.identity = ProfileIdentity(
            profile_uuid="prof_001",
            symbol="BTC",
            timeframe="1m",
            window="SESSION",
            calendar="24x7",
            binning_policy="FIXED_1.0"
        )
        self.engine = TPOProfileEngine(self.identity, bin_size=1.0)
        self.tc = TemporalContext(1.0, 1.0, 1.0, 1.0)

    def test_accumulator_updates_incrementally(self):
        """Verifies TPO accumulator correctly assigns bin density."""
        bar1 = Bar("BTC", self.tc, 100.0, 102.0, 100.0, 101.0, 10.0)
        
        self.engine.process_sample(bar1)
        
        hist = self.engine.accumulator.histogram
        self.assertIn(100.0, hist)
        self.assertIn(101.0, hist)
        self.assertIn(102.0, hist)
        self.assertEqual(hist[100.0], 1)
        
        # Test POC update
        bar2 = Bar("BTC", self.tc, 100.0, 100.0, 100.0, 100.0, 10.0)
        self.engine.process_sample(bar2)
        
        self.assertEqual(hist[100.0], 2)
        self.assertEqual(self.engine.accumulator.poc_price, 100.0)

    def test_snapshot_restoration(self):
        """Verifies engine can instantly restore state from snapshot."""
        bar = Bar("BTC", self.tc, 50.0, 50.0, 50.0, 50.0, 1.0)
        self.engine.process_sample(bar)
        
        snapshot = self.engine.create_checkpoint()
        
        # Create a brand new engine
        new_engine = TPOProfileEngine(self.identity, bin_size=1.0)
        new_engine.restore_checkpoint(snapshot)
        
        # Verify state is completely synchronized
        self.assertEqual(new_engine.accumulator.poc_price, 50.0)
        self.assertEqual(new_engine.accumulator.histogram[50.0], 1)

if __name__ == '__main__':
    unittest.main()
