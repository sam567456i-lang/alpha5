import unittest
from datetime import datetime
from Backend.core.evidence_dtos.imbalance import FVG, ImbalanceLifecycleState
from Backend.core.analytical_rules.imbalance_rules import ImbalanceExtractionRule

class TestImbalanceObjects(unittest.TestCase):
    
    def setUp(self):
        self.extractor = ImbalanceExtractionRule()
        self.now = datetime.now()

    def test_bullish_fvg_extraction(self):
        """Verify mathematical extraction of Bullish FVG from pure OHLC data."""
        bar1 = {'high': 100.0, 'low': 90.0}
        bar2 = {'high': 120.0, 'low': 95.0} # Gap happens here
        bar3 = {'high': 130.0, 'low': 110.0} # Bar 3 low > Bar 1 high
        
        fvgs = self.extractor.extract_fvg(bar1, bar2, bar3, self.now)
        self.assertEqual(len(fvgs), 1)
        
        fvg = fvgs[0]
        self.assertIsInstance(fvg, FVG)
        
        # Geometry verification
        self.assertEqual(fvg.lower_bound, 100.0)
        self.assertEqual(fvg.upper_bound, 110.0)
        self.assertEqual(fvg.height, 10.0)
        self.assertEqual(fvg.fill_percent, 0.0)
        self.assertEqual(fvg.remaining_percent, 1.0)
        
        # Lifecycle state
        self.assertEqual(fvg.lifecycle_state, ImbalanceLifecycleState.ACTIVE)
        
    def test_bearish_fvg_extraction(self):
        """Verify mathematical extraction of Bearish FVG from pure OHLC data."""
        bar1 = {'high': 130.0, 'low': 110.0}
        bar2 = {'high': 120.0, 'low': 90.0}
        bar3 = {'high': 100.0, 'low': 80.0} # Bar 3 high < Bar 1 low
        
        fvgs = self.extractor.extract_fvg(bar1, bar2, bar3, self.now)
        self.assertEqual(len(fvgs), 1)
        
        fvg = fvgs[0]
        self.assertIsInstance(fvg, FVG)
        self.assertEqual(fvg.upper_bound, 110.0)
        self.assertEqual(fvg.lower_bound, 100.0)
        self.assertEqual(fvg.height, 10.0)

    def test_no_fvg_extraction(self):
        """Verify no FVG is created when price action overlaps completely."""
        bar1 = {'high': 100.0, 'low': 90.0}
        bar2 = {'high': 105.0, 'low': 95.0}
        bar3 = {'high': 110.0, 'low': 95.0} # Bar 3 low < Bar 1 high (Overlap)
        
        fvgs = self.extractor.extract_fvg(bar1, bar2, bar3, self.now)
        self.assertEqual(len(fvgs), 0)

if __name__ == '__main__':
    unittest.main()
