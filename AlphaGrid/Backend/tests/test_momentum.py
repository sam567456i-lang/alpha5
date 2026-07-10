import unittest
import math
from typing import Iterator
from Backend.core.interfaces.market_data import BarView, Bar, TemporalContext
from Backend.core.interfaces.math_backend import MathBackend, NumericalPolicy
from Backend.core.evidence_dtos.momentum import MomentumPolicy, VelocityPolicy
from Backend.core.analytical_rules.momentum_rules import MomentumEngine

class PythonMathBackend(MathBackend):
    def supports_vectorization(self) -> bool: return False
    def supports_gpu(self) -> bool: return False
    def supports_parallel(self) -> bool: return False
    def supports_streaming(self) -> bool: return True
    
    def apply_numerical_policy(self, value: float, policy: NumericalPolicy) -> float:
        if math.isnan(value) or math.isinf(value):
            return 0.0 # Simplistic handling for test
        if abs(value) < policy.zero_threshold:
            return 0.0
        return value

class MockBarView(BarView):
    def __init__(self, current_bar: Bar):
        self.bar = current_bar
    def latest(self) -> Bar: return self.bar
    def previous(self, n: int = 1) -> Bar: return self.bar
    def window(self, size: int) -> 'MarketDataView': return self
    def slice(self, start: int, end: int) -> 'MarketDataView': return self
    def lookback(self, seconds: float) -> 'MarketDataView': return self
    def iterator(self) -> Iterator[Bar]: yield self.bar
    def __len__(self) -> int: return 1

class TestMomentum(unittest.TestCase):
    
    def setUp(self):
        self.backend = PythonMathBackend()
        self.policy = MomentumPolicy(velocity_policy=VelocityPolicy(lookback_window=3))
        self.engine = MomentumEngine(self.backend, self.policy)
        
    def _create_bar(self, close: float, ts: float) -> Bar:
        tc = TemporalContext(event_time=ts, exchange_time=ts, receive_time=ts, replay_time=ts)
        return Bar(symbol="BTC", temporal_context=tc, open_price=close, high_price=close, low_price=close, close_price=close, volume=100.0)

    def test_streaming_velocity(self):
        """Verifies O(1) streaming builds velocity correctly across window."""
        b1 = self._create_bar(100.0, 1.0)
        b2 = self._create_bar(105.0, 2.0)
        b3 = self._create_bar(110.0, 3.0)
        
        # Pushing b1
        self.assertIsNone(self.engine.process_tick_stream(MockBarView(b1)))
        
        # Pushing b2
        self.assertIsNone(self.engine.process_tick_stream(MockBarView(b2)))
        
        # Pushing b3 (Window filled, but we don't have N periods of distance yet)
        self.assertIsNone(self.engine.process_tick_stream(MockBarView(b3)))
        
        # Pushing b4 (115). Oldest was 100.
        b4 = self._create_bar(115.0, 4.0)
        mo2 = self.engine.process_tick_stream(MockBarView(b4))
        self.assertIsNotNone(mo2)
        
        # Velocity = 115 - 100 = 15
        self.assertEqual(mo2.velocity.absolute_velocity, 15.0)
        self.assertEqual(mo2.rate_of_change.roc_percentage, 0.15) # 15 / 100 = 15%
        self.assertEqual(mo2.acceleration.acceleration, 0.0) # Acceleration needs two velocity data points

    def test_zero_price_protection(self):
        """Verifies engine protects against Division By Zero via NumericalPolicy."""
        # Force the oldest price to 0.0
        b1 = self._create_bar(0.0, 1.0)
        b2 = self._create_bar(0.0, 2.0)
        b3 = self._create_bar(10.0, 3.0)
        b4 = self._create_bar(10.0, 4.0)
        
        self.engine.process_tick_stream(MockBarView(b1))
        self.engine.process_tick_stream(MockBarView(b2))
        self.engine.process_tick_stream(MockBarView(b3))
        mo = self.engine.process_tick_stream(MockBarView(b4))
        
        # It should compute successfully, clamping oldest to epsilon (e.g. 1e-9)
        self.assertIsNotNone(mo)
        self.assertEqual(mo.velocity.absolute_velocity, 10.0)
        # ROC will be massive (10 / 1e-9) but not crash
        self.assertTrue(mo.rate_of_change.roc_percentage > 1000000)

if __name__ == '__main__':
    unittest.main()
