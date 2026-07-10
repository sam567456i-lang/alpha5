import unittest
from Backend.core.interfaces.capabilities import FeedManifest, FeedCapability, CapabilityLevel
from Backend.core.interfaces.market_data import Trade, TemporalContext
from Backend.core.evidence_dtos.order_flow import TradeClassificationPolicy, TradeClassificationRule
from Backend.core.analytical_rules.order_flow_rules import OrderFlowEngine

class TestOrderFlowEngine(unittest.TestCase):
    def setUp(self):
        # Provide ONLY Trade capabilities (No Level2)
        self.manifest = FeedManifest(provider_name="BasicBroker", capabilities={FeedCapability.TRADE})
        self.policy = TradeClassificationPolicy(rule=TradeClassificationRule.TICK_RULE)
        self.engine = OrderFlowEngine(self.manifest, self.policy)

    def test_capability_degradation(self):
        """Verifies Iceberg and Absorption modules silently degrade to UNSUPPORTED, avoiding a crash."""
        self.assertEqual(self.engine.delta_capability, CapabilityLevel.SUPPORTED)
        self.assertEqual(self.engine.iceberg_capability, CapabilityLevel.UNSUPPORTED)
        self.assertEqual(self.engine.absorption_capability, CapabilityLevel.UNSUPPORTED)

    def test_tick_rule_delta(self):
        """Verifies TICK_RULE successfully derives buyer-initiated trades to calculate Delta."""
        tc = TemporalContext(1.0, 1.0, 1.0, 1.0)
        
        # Base trade at 100
        t1 = Trade("BTC", tc, price=100.0, size=1.0, is_buyer_maker=False)
        self.engine.process_trade(t1)
        
        # Uptick to 101 -> Buyer initiated -> Ask Volume -> Positive Delta
        t2 = Trade("BTC", tc, price=101.0, size=5.0, is_buyer_maker=False)
        delta2 = self.engine.process_trade(t2)
        
        self.assertIsNotNone(delta2)
        self.assertEqual(delta2.net_delta, 5.0)
        self.assertEqual(delta2.ask_volume, 5.0)
        self.assertEqual(delta2.bid_volume, 0.0)
        
        # Downtick to 99 -> Seller initiated -> Bid Volume -> Negative Delta
        t3 = Trade("BTC", tc, price=99.0, size=3.0, is_buyer_maker=False)
        delta3 = self.engine.process_trade(t3)
        
        self.assertEqual(delta3.net_delta, -3.0)
        self.assertEqual(delta3.bid_volume, 3.0)
        
        # CVD should aggregate
        self.assertEqual(self.engine.current_cvd, 3.0) # 1 (t1) + 5 (t2) - 3 (t3) = 3.0

if __name__ == '__main__':
    unittest.main()
