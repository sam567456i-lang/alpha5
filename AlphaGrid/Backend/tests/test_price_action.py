import unittest
from datetime import datetime, timedelta
from Backend.core.evidence_dtos.price_action import Doji, Engulfing, NR4
from Backend.core.analytical_rules.price_action_rules import PriceActionEngine

class TestPriceAction(unittest.TestCase):
    
    def setUp(self):
        self.engine = PriceActionEngine()
        self.now = datetime.now()

    def test_doji_extraction(self):
        """Mathematically verifies an open/close distance < 5% of spread generates a Doji."""
        # 10 point spread, 0.2 point body (2% of spread)
        bar = {"open": 95.0, "high": 100.0, "low": 90.0, "close": 95.2, "timestamp": self.now}
        
        events = self.engine.extract_single_candle(bar, atr=10.0)
        self.assertEqual(len(events), 1)
        self.assertIsInstance(events[0], Doji)
        self.assertAlmostEqual(events[0].open_close_distance, 0.2, places=2)

    def test_no_doji_on_large_body(self):
        """Verifies large body rejects Doji creation."""
        # 10 point spread, 5.0 point body (50% of spread)
        bar = {"open": 90.0, "high": 100.0, "low": 90.0, "close": 95.0, "timestamp": self.now}
        
        events = self.engine.extract_single_candle(bar, atr=10.0)
        self.assertEqual(len(events), 0)

    def test_engulfing_extraction(self):
        """Verifies bar 2 body completely covering bar 1 body triggers Engulfing."""
        bar1 = {"open": 95.0, "high": 96.0, "low": 93.0, "close": 94.0, "timestamp": self.now - timedelta(minutes=5)} # 1 point body
        bar2 = {"open": 93.0, "high": 97.0, "low": 92.0, "close": 96.0, "timestamp": self.now} # 3 point body, wraps [94,95] inside [93,96]
        
        events = self.engine.extract_two_candle(bar1, bar2)
        self.assertEqual(len(events), 1)
        self.assertIsInstance(events[0], Engulfing)
        self.assertEqual(events[0].geometric_upper_bound, 97.0)
        self.assertEqual(events[0].geometric_lower_bound, 92.0)

    def test_nr4_extraction(self):
        """Verifies narrowest range of last 4 bars fires NR4."""
        b1 = {"high": 10.0, "low": 5.0, "timestamp": self.now - timedelta(minutes=15)} # Range 5
        b2 = {"high": 12.0, "low": 6.0, "timestamp": self.now - timedelta(minutes=10)} # Range 6
        b3 = {"high": 11.0, "low": 7.0, "timestamp": self.now - timedelta(minutes=5)}  # Range 4
        b4 = {"high": 9.0,  "low": 7.0, "timestamp": self.now}                         # Range 2 (Smallest)
        
        lookback = [b1, b2, b3, b4]
        events = self.engine.extract_range_patterns(lookback)
        
        self.assertEqual(len(events), 1)
        self.assertIsInstance(events[0], NR4)
        self.assertEqual(events[0].range_value, 2.0)

if __name__ == '__main__':
    unittest.main()
