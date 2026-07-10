import unittest
from Backend.core.engines.range.boundary_engine import BoundaryEngine
from Backend.core.engines.range.geometry_engine import GeometryEngine

class TestRangeFamily(unittest.TestCase):
    
    def setUp(self):
        self.boundary_engine = BoundaryEngine()
        self.geometry_engine = GeometryEngine()

    def test_structural_boundary_generation(self):
        """Test that alternating pivots generate a range boundary."""
        pivot_1 = {
            "state": "Confirmed", "pivot_type": "High",
            "price": 100.0, "timestamp": 10
        }
        pivot_2 = {
            "state": "Confirmed", "pivot_type": "Low",
            "price": 80.0, "timestamp": 20
        }
        
        ev1 = self.boundary_engine.process_event(pivot_1)
        self.assertIsNone(ev1) # Need two alternating
        
        ev2 = self.boundary_engine.process_event(pivot_2)
        self.assertIsNotNone(ev2)
        self.assertEqual(ev2.range_high, 100.0)
        self.assertEqual(ev2.range_low, 80.0)
        self.assertEqual(ev2.midpoint, 90.0)
        self.assertEqual(ev2.origin_timestamp, 10)

    def test_same_type_pivots_ignored(self):
        """Test that two High pivots do not form a new structural range boundary directly (Swing handles EQH)."""
        pivot_1 = {
            "state": "Confirmed", "pivot_type": "High",
            "price": 100.0, "timestamp": 10
        }
        pivot_2 = {
            "state": "Confirmed", "pivot_type": "High",
            "price": 105.0, "timestamp": 20
        }
        
        self.boundary_engine.process_event(pivot_1)
        ev2 = self.boundary_engine.process_event(pivot_2)
        self.assertIsNone(ev2)

    def test_geometry_and_numerical_stability(self):
        """Test geometry calculations, including zero-width ranges."""
        boundary_event = {
            "range_high": 100.0,
            "range_low": 100.0, # Zero width
            "midpoint": 100.0,
            "origin_timestamp": 10
        }
        
        geom = self.geometry_engine.process_event(boundary_event, current_timestamp=50, tick_size=0.01)
        
        self.assertEqual(geom.width_ticks, 0.0)
        self.assertEqual(geom.width_percentage, 0.0)
        self.assertEqual(geom.duration_bars, 40)

if __name__ == "__main__":
    unittest.main()
