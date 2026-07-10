import unittest
from datetime import datetime
from Backend.core.methodologies.core_models import MethodologyContext, MethodologyDefinition, MethodologyVersion
from Backend.core.methodologies.instances.trend import TrendAlignmentRule, TrendFollowingMethodology
from Backend.core.methodologies.state_machine import LifecycleState

class TestTrendV1(unittest.TestCase):
    def setUp(self):
        self.context = MethodologyContext(
            context_id="ctx_001",
            symbol="BTCUSDT",
            timeframe="1H",
            execution_timestamp=datetime.now(),
            market_regime="TREND",
            available_capabilities=["Trend"],
            object_graph_snapshot={},
            feature_snapshot={"trend.strength.v1": 0.8},
            data_quality_score=0.99,
            degradation_state="NONE"
        )
        self.definition = MethodologyDefinition("trend", "Trend", "Trend Def")
        self.version = MethodologyVersion(self.definition, "v1.0", "r1")
        
    def test_layer1_rule_functional_validation(self):
        """Layer 1: Tests the atomic rule in isolation."""
        rule = TrendAlignmentRule()
        ev = rule.evaluate(self.context)
        self.assertIsNotNone(ev)
        self.assertEqual(ev.confidence, 0.8)
        self.assertEqual(ev.provenance.direct_weight, 1.0)
        
    def test_layer2_methodology_integration(self):
        """Layer 2: Tests methodology orchestrates rules into State Transitions and Claims."""
        instance = TrendFollowingMethodology("inst_1", self.version, "BTCUSDT", "1H")
        claims = instance.evaluate(self.context)
        
        self.assertEqual(len(claims), 1)
        self.assertEqual(claims[0].claim_type, "BullishContinuation")
        
        # Verify State Machine transition
        self.assertEqual(instance.state_machine.current_state, LifecycleState.ESTABLISHED)
        self.assertEqual(len(instance.state_machine.transition_history), 1)
        
if __name__ == '__main__':
    unittest.main()
