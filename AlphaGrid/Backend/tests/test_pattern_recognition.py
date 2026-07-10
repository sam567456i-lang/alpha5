import unittest
from datetime import datetime
from Backend.core.evidence_dtos.pattern_components import DoubleTopPolicy, Peak, Neckline
from Backend.core.evidence_dtos.pattern_recognition import DoubleTop, PatternLifecycleState
from Backend.core.analytical_rules.pattern_rules import PatternRecognitionEngine

class TestPatternRecognition(unittest.TestCase):
    
    def setUp(self):
        self.engine = PatternRecognitionEngine()
        self.policy = DoubleTopPolicy(max_peak_variance_pct=0.005, min_neckline_depth_pct=0.02) # 0.5% variance, 2% pullback
        self.now = datetime.now()

    def test_double_top_extraction(self):
        """Verifies policy-driven extraction of Double Top components."""
        sh1 = {"price": 100.0, "timestamp": self.now.timestamp()}
        sl1 = {"price": 95.0, "timestamp": self.now.timestamp() + 10} # 5% depth
        sh2 = {"price": 100.2, "timestamp": self.now.timestamp() + 20} # 0.2% variance
        
        events = self.engine.evaluate_double_top(sh1, sl1, sh2, self.policy, self.now)
        
        self.assertEqual(len(events), 1)
        dt = events[0]
        self.assertIsInstance(dt, DoubleTop)
        
        # Verify Component aggregation
        self.assertIsInstance(dt.peak1, Peak)
        self.assertIsInstance(dt.peak2, Peak)
        self.assertIsInstance(dt.neckline, Neckline)
        
        # Verify Math Constraints
        self.assertEqual(dt.peak1.price_level, 100.0)
        self.assertEqual(dt.peak2.price_level, 100.2)
        self.assertEqual(dt.neckline.y_intercept, 95.0)
        
        # Verify Quality math
        self.assertAlmostEqual(dt.quality.geometric_error, 0.001996, places=5)
        self.assertEqual(dt.lifecycle_state, PatternLifecycleState.CANDIDATE)

    def test_double_top_variance_rejection(self):
        """Verifies strict adherence to Geometry Policies (rejecting loose tops)."""
        sh1 = {"price": 100.0, "timestamp": self.now.timestamp()}
        sl1 = {"price": 95.0, "timestamp": self.now.timestamp() + 10} 
        sh2 = {"price": 101.0, "timestamp": self.now.timestamp() + 20} # 1.0% variance (Violates 0.5% max)
        
        events = self.engine.evaluate_double_top(sh1, sl1, sh2, self.policy, self.now)
        self.assertEqual(len(events), 0) # Engine must reject building the pattern

if __name__ == '__main__':
    unittest.main()
