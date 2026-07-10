import unittest
from Backend.core.engines.trend.direction_engine import DirectionEngine
from Backend.core.engines.trend.geometry_engine import GeometryEngine

class TestTrendFamily(unittest.TestCase):
    
    def setUp(self):
        self.dir_engine = DirectionEngine()
        self.geo_engine = GeometryEngine()

    def test_direction_engine_thresholds(self):
        # Slope > 0.005 -> Up
        ev_up = self.dir_engine.process_event({"slope": 0.01})
        self.assertEqual(ev_up.direction, "Up")
        
        # Slope < -0.005 -> Down
        ev_down = self.dir_engine.process_event({"slope": -0.01})
        self.assertEqual(ev_down.direction, "Down")
        
        # Slope inside threshold -> Neutral
        ev_neutral = self.dir_engine.process_event({"slope": 0.001})
        self.assertEqual(ev_neutral.direction, "Neutral")

    def test_geometry_engine_derivatives(self):
        # Step 1: Initialize
        self.geo_engine.process_event({"rolling_mean": 100})
        
        # Step 2: Linear increase (slope = +2, accel = 0)
        res1 = self.geo_engine.process_event({"rolling_mean": 102})
        self.assertEqual(res1["slope"].slope, 2.0)
        self.assertEqual(res1["acceleration"].acceleration, 2.0) # 2.0 - 0.0
        
        # Step 3: Accelerating increase (slope = +4, accel = +2)
        res2 = self.geo_engine.process_event({"rolling_mean": 106})
        self.assertEqual(res2["slope"].slope, 4.0)
        self.assertEqual(res2["acceleration"].acceleration, 2.0)

    # --- Family Acceptance Datasets (Integration level expectations) ---
    
    def test_dataset_a_constant_prices(self):
        """Dataset A: Constant prices -> Neutral, Weak"""
        res = self.dir_engine.process_event({"slope": 0.0})
        self.assertEqual(res.direction, "Neutral")

    def test_dataset_b_linear_increase(self):
        """Dataset B: Linear increase -> Up, Slope Constant, Accel 0"""
        self.geo_engine.process_event({"rolling_mean": 10})
        r1 = self.geo_engine.process_event({"rolling_mean": 20}) # slope 10
        r2 = self.geo_engine.process_event({"rolling_mean": 30}) # slope 10, accel 0
        self.assertEqual(r2["slope"].slope, 10.0)
        self.assertEqual(r2["acceleration"].acceleration, 0.0)
        
        d = self.dir_engine.process_event({"slope": r2["slope"].slope})
        self.assertEqual(d.direction, "Up")

    def test_dataset_c_accelerating_trend(self):
        """Dataset C: Accelerating trend -> Up, Accel > 0"""
        self.geo_engine.process_event({"rolling_mean": 10})
        self.geo_engine.process_event({"rolling_mean": 20}) # slope 10
        r2 = self.geo_engine.process_event({"rolling_mean": 35}) # slope 15, accel 5
        self.assertEqual(r2["slope"].slope, 15.0)
        self.assertTrue(r2["acceleration"].acceleration > 0)

    # --- Numerical Stability Tests ---
    
    def test_geometry_flat_slope_stability(self):
        # Flat slope should not cause divide by zero
        self.geo_engine.process_event({"rolling_mean": 50})
        res = self.geo_engine.process_event({"rolling_mean": 50})
        self.assertEqual(res["slope"].slope, 0.0)

if __name__ == "__main__":
    unittest.main()
