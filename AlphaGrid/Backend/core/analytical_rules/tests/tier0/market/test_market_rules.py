import unittest
from Backend.core.analytical_rules.dto.rule_context_dto import RuleContextDTO
from Backend.core.interfaces.execution_mode_dto import ExecutionModeDTO
from Backend.core.analytical_rules.implementations.tier0.market.trend_rule import TrendRule
from Backend.core.analytical_rules.implementations.tier0.market.structure_rule import StructureRule
from Backend.core.analytical_rules.implementations.tier0.market.volatility_rule import VolatilityRule
from Backend.core.analytical_rules.implementations.tier0.market.liquidity_rule import LiquidityRule

class TestMarketRules(unittest.TestCase):
    
    def setUp(self):
        self.context = RuleContextDTO(
            concept_references=["CONCEPT-M-001", "CONCEPT-M-002"],
            methodology_context_id="CTX-003",
            execution_mode=ExecutionModeDTO(mode="Standard", description="Standard Testing"),
            registry_versions={"analytical_rule_registry": "1.0.0"}
        )

    def test_trend_rule(self):
        rule = TrendRule()
        evidence = rule.evaluate(self.context)
        self.assertEqual(evidence.identity.producer_rule, "RULE-T0-009")
        self.assertEqual(evidence.evidence_data["trend_direction"], "Bullish")
        self.assertEqual(evidence.evidence_type, "TrendEvidence")

    def test_structure_rule(self):
        rule = StructureRule()
        evidence = rule.evaluate(self.context)
        self.assertEqual(evidence.identity.producer_rule, "RULE-T0-010")
        self.assertTrue(evidence.evidence_data["bos"])
        self.assertEqual(evidence.evidence_type, "StructureEvidence")

    def test_volatility_rule(self):
        rule = VolatilityRule()
        evidence = rule.evaluate(self.context)
        self.assertEqual(evidence.identity.producer_rule, "RULE-T0-011")
        self.assertEqual(evidence.evidence_data["regime"], "Expansion")
        self.assertEqual(evidence.evidence_type, "VolatilityEvidence")

    def test_liquidity_rule(self):
        rule = LiquidityRule()
        evidence = rule.evaluate(self.context)
        self.assertEqual(evidence.identity.producer_rule, "RULE-T0-012")
        self.assertTrue(evidence.evidence_data["bsl_present"])
        self.assertEqual(evidence.evidence_data["draw_on_liquidity"], "BSL")
        self.assertEqual(evidence.evidence_type, "LiquidityEvidence")

if __name__ == "__main__":
    unittest.main()
