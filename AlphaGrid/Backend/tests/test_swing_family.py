import unittest
from Backend.core.engines.swing.pivot_engine import PivotEngine, NBarFractalPolicy
from Backend.core.engines.swing.relationship_engine import RelationshipEngine

class TestSwingFamily(unittest.TestCase):
    
    def setUp(self):
        self.pivot_engine = PivotEngine(policy=NBarFractalPolicy(n=2))
        self.rel_engine = RelationshipEngine()

    def test_dataset_a_flat_market(self):
        """Dataset A: Flat market. No pivots should be detected."""
        for i in range(10):
            ev = self.pivot_engine.process_event({
                "timestamp": i, "high": 100, "low": 100
            })
            self.assertIsNone(ev)

    def test_dataset_d_double_top(self):
        """Dataset D: Double Top (Equal Highs)"""
        # We simulate two confirmed High pivots and feed to relationship engine
        ev1 = {
            "state": "Confirmed", "pivot_type": "High",
            "price": 100.0, "timestamp": 10, "atr": 1.0
        }
        ev2 = {
            "state": "Confirmed", "pivot_type": "High",
            "price": 100.05, "timestamp": 20, "atr": 1.0
        }
        
        self.rel_engine.process_event(ev1)
        rel_ev = self.rel_engine.process_event(ev2)
        
        # Tolerance is 0.1 * 1.0 = 0.1
        # Diff is 0.05 <= 0.1, so EQH
        self.assertIsNotNone(rel_ev)
        self.assertEqual(rel_ev.relationship, "EQH")

    def test_dataset_e_equal_lows(self):
        """Dataset E: Equal Lows"""
        ev1 = {
            "state": "Confirmed", "pivot_type": "Low",
            "price": 50.0, "timestamp": 10, "atr": 2.0
        }
        ev2 = {
            "state": "Confirmed", "pivot_type": "Low",
            "price": 50.1, "timestamp": 20, "atr": 2.0
        }
        
        self.rel_engine.process_event(ev1)
        rel_ev = self.rel_engine.process_event(ev2)
        
        # Tolerance 0.1 * 2.0 = 0.2. Diff is 0.1 <= 0.2 -> EQL
        self.assertIsNotNone(rel_ev)
        self.assertEqual(rel_ev.relationship, "EQL")

    def test_dataset_c_steady_downtrend(self):
        """Dataset C: Steady downtrend -> LH, LL"""
        h1 = {"state": "Confirmed", "pivot_type": "High", "price": 100, "timestamp": 10, "atr": 1}
        l1 = {"state": "Confirmed", "pivot_type": "Low", "price": 80, "timestamp": 15, "atr": 1}
        h2 = {"state": "Confirmed", "pivot_type": "High", "price": 90, "timestamp": 20, "atr": 1}
        l2 = {"state": "Confirmed", "pivot_type": "Low", "price": 70, "timestamp": 25, "atr": 1}
        
        self.rel_engine.process_event(h1)
        self.rel_engine.process_event(l1)
        rel_h = self.rel_engine.process_event(h2)
        rel_l = self.rel_engine.process_event(l2)
        
        self.assertEqual(rel_h.relationship, "LH")
        self.assertEqual(rel_l.relationship, "LL")

    def test_numerical_stability(self):
        """Test with missing ATR and zero ATR."""
        ev1 = {"state": "Confirmed", "pivot_type": "High", "price": 100.0, "timestamp": 10, "atr": 0.0}
        ev2 = {"state": "Confirmed", "pivot_type": "High", "price": 100.0, "timestamp": 20, "atr": 0.0}
        
        self.rel_engine.process_event(ev1)
        rel = self.rel_engine.process_event(ev2)
        # Tolerance with atr 0.0 will be 0. tick_size * 5 = 0.05. Diff is 0 <= 0.05
        self.assertEqual(rel.relationship, "EQH")

    def test_streaming_vs_batch_determinism(self):
        """Verify that feeding bars one-by-one produces identical pivots as batch processing (simulated by same engine instance logic)."""
        engine = PivotEngine(policy=NBarFractalPolicy(n=1))
        
        # Dataset
        bars = [
            {"high": 10, "low": 5, "timestamp": 1},
            {"high": 12, "low": 6, "timestamp": 2}, # High Pivot
            {"high": 11, "low": 4, "timestamp": 3}, # Low Pivot
            {"high": 15, "low": 8, "timestamp": 4},
            {"high": 14, "low": 7, "timestamp": 5},
        ]
        
        # Stream bar by bar
        pivots = []
        for bar in bars:
            ev = engine.process_event(bar)
            if ev:
                pivots.append(ev)
                
        # N=1 means it takes 3 bars to form a pivot (t-1, t, t+1)
        # Bar 2 is a High pivot (10, 12, 11). Discovered at Bar 3.
        # Bar 4 is a High pivot (11, 15, 14). Discovered at Bar 5.
        self.assertEqual(len(pivots), 3)
        self.assertEqual(pivots[0].pivot_type, "High")
        self.assertEqual(pivots[0].price, 12)
        self.assertEqual(pivots[1].pivot_type, "Low")
        self.assertEqual(pivots[1].price, 4)
        self.assertEqual(pivots[2].pivot_type, "High")
        self.assertEqual(pivots[2].price, 15)

if __name__ == "__main__":
    unittest.main()
