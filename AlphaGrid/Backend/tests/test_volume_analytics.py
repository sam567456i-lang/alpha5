import unittest
from datetime import datetime
from Backend.core.evidence_dtos.volume_analytics import ClimaxVolume, BuyingPressure, SellingPressure
from Backend.core.analytical_rules.volume_rules import VolumeAnalyticsEngine

class TestVolumeAnalytics(unittest.TestCase):
    
    def setUp(self):
        self.engine = VolumeAnalyticsEngine()
        self.now = datetime.now()
        self.avg_vol = 1000.0
        self.std_vol = 200.0

    def test_climax_volume_detection(self):
        """Mathematically verifies > 2.5 SD fires ClimaxVolume."""
        # 1000 + (2.6 * 200) = 1520
        bar = {"volume": 1520.0, "high": 10.0, "low": 9.0, "close": 9.5}
        
        events = self.engine.analyze_volume(bar, self.avg_vol, self.std_vol, self.now)
        
        # We expect a ClimaxVolume but no Pressure (since close is exactly middle 50%)
        self.assertEqual(len(events), 1)
        self.assertIsInstance(events[0], ClimaxVolume)
        self.assertEqual(events[0].standard_deviations, 2.6)

    def test_buying_pressure_detection(self):
        """Verifies high volume + top 25% close fires BuyingPressure."""
        # Volume > 1.5 SD (e.g., 1000 + 1.6*200 = 1320)
        # Close near high
        bar = {"volume": 1320.0, "high": 100.0, "low": 90.0, "close": 98.0}
        
        events = self.engine.analyze_volume(bar, self.avg_vol, self.std_vol, self.now)
        
        # Climax > 2.5 isn't met, but > 1.5 is met. BuyingPressure should fire.
        self.assertEqual(len(events), 1)
        self.assertIsInstance(events[0], BuyingPressure)
        self.assertEqual(events[0].close_percentage, 0.8) # (98-90)/10 = 0.8

    def test_selling_pressure_detection(self):
        """Verifies high volume + bottom 25% close fires SellingPressure."""
        # Volume > 1.5 SD (e.g., 1320)
        # Close near low
        bar = {"volume": 1320.0, "high": 100.0, "low": 90.0, "close": 91.0}
        
        events = self.engine.analyze_volume(bar, self.avg_vol, self.std_vol, self.now)
        
        self.assertEqual(len(events), 1)
        self.assertIsInstance(events[0], SellingPressure)
        self.assertEqual(events[0].close_percentage, 0.1) # (91-90)/10 = 0.1

    def test_missing_volume_data(self):
        """Engine MUST actively reject ticks missing volume data."""
        bar = {"high": 100.0, "low": 90.0, "close": 91.0} # No volume
        
        with self.assertRaises(ValueError):
            self.engine.analyze_volume(bar, self.avg_vol, self.std_vol, self.now)

if __name__ == '__main__':
    unittest.main()
