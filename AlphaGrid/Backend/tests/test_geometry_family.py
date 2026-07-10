import unittest
from Backend.core.engines.geometry.distance_engine import DistanceEngine
from Backend.core.engines.geometry.containment_engine import ContainmentEngine

class TestGeometryFamily(unittest.TestCase):
    
    def setUp(self):
        self.distance_engine = DistanceEngine()
        self.containment_engine = ContainmentEngine()

    def test_distance_calculation(self):
        """Test calculation of distance between two pivots."""
        pivot_1 = {
            "pivot_type": "Low", "price": 100.0, "timestamp": 10
        }
        pivot_2 = {
            "pivot_type": "High", "price": 110.0, "timestamp": 20
        }
        
        dist = self.distance_engine.process_event(pivot_1, pivot_2, atr=2.0, tick_size=0.1)
        
        self.assertEqual(dist.distance_price, 10.0)
        self.assertEqual(dist.distance_time, 10)
        self.assertEqual(dist.distance_ticks, 100.0)
        self.assertEqual(dist.distance_atr, 5.0)

    def test_containment_logic(self):
        """Test containment logic."""
        range_bnd = {
            "range_high": 110.0, "range_low": 90.0, "midpoint": 100.0
        }
        
        # Test 1: Inside
        cont_in = self.containment_engine.process_event(price=105.0, timestamp=30, range_boundary=range_bnd)
        self.assertTrue(cont_in.is_contained)
        self.assertEqual(cont_in.containment_percentage, 0.75)
        
        # Test 2: Outside High
        cont_out = self.containment_engine.process_event(price=115.0, timestamp=30, range_boundary=range_bnd)
        self.assertFalse(cont_out.is_contained)
        self.assertEqual(cont_out.containment_percentage, 1.25)

    def test_numerical_stability(self):
        """Test containment in a zero-width range."""
        range_bnd = {
            "range_high": 100.0, "range_low": 100.0, "midpoint": 100.0
        }
        
        # At boundary
        cont_at = self.containment_engine.process_event(price=100.0, timestamp=30, range_boundary=range_bnd)
        self.assertTrue(cont_at.is_contained)
        self.assertEqual(cont_at.containment_percentage, 1.0)
        
        # Outside boundary
        cont_out = self.containment_engine.process_event(price=101.0, timestamp=30, range_boundary=range_bnd)
        self.assertFalse(cont_out.is_contained)
        self.assertEqual(cont_out.containment_percentage, 0.0)

if __name__ == "__main__":
    unittest.main()
