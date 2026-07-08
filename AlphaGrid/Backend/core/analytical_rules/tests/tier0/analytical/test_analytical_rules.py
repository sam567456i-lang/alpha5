import unittest
from Backend.core.analytical_rules.dto.rule_context_dto import RuleContextDTO
from Backend.core.interfaces.execution_mode_dto import ExecutionModeDTO
from Backend.core.analytical_rules.implementations.tier0.analytical.premium_rule import PremiumRule
from Backend.core.analytical_rules.implementations.tier0.analytical.discount_rule import DiscountRule
from Backend.core.analytical_rules.implementations.tier0.analytical.equilibrium_rule import EquilibriumRule
from Backend.core.analytical_rules.implementations.tier0.analytical.mean_reversion_rule import MeanReversionRule
from Backend.core.analytical_rules.implementations.tier0.analytical.freshness_rule import FreshnessRule
from Backend.core.analytical_rules.implementations.tier0.analytical.quality_rule import QualityRule
from Backend.core.analytical_rules.implementations.tier0.analytical.context_alignment_rule import ContextAlignmentRule
from Backend.core.analytical_rules.implementations.tier0.analytical.confluence_rule import ConfluenceRule

class TestAnalyticalRules(unittest.TestCase):
    
    def setUp(self):
        self.context = RuleContextDTO(
            concept_references=["CONCEPT-A-001", "CONCEPT-A-002"],
            methodology_context_id="CTX-004",
            execution_mode=ExecutionModeDTO(mode="Standard", description="Standard Testing"),
            registry_versions={"analytical_rule_registry": "1.0.0"}
        )

    def test_premium_rule(self):
        rule = PremiumRule()
        evidence = rule.evaluate(self.context)
        self.assertEqual(evidence.identity.producer_rule, "RULE-T0-013")
        self.assertTrue(evidence.evidence_data["is_premium"])

    def test_discount_rule(self):
        rule = DiscountRule()
        evidence = rule.evaluate(self.context)
        self.assertEqual(evidence.identity.producer_rule, "RULE-T0-014")
        self.assertFalse(evidence.evidence_data["is_discount"])

    def test_equilibrium_rule(self):
        rule = EquilibriumRule()
        evidence = rule.evaluate(self.context)
        self.assertEqual(evidence.identity.producer_rule, "RULE-T0-015")
        self.assertFalse(evidence.evidence_data["is_equilibrium"])

    def test_mean_reversion_rule(self):
        rule = MeanReversionRule()
        evidence = rule.evaluate(self.context)
        self.assertEqual(evidence.identity.producer_rule, "RULE-T0-016")
        self.assertTrue(evidence.evidence_data["reverting"])

    def test_freshness_rule(self):
        rule = FreshnessRule()
        evidence = rule.evaluate(self.context)
        self.assertEqual(evidence.identity.producer_rule, "RULE-T0-017")
        self.assertTrue(evidence.evidence_data["untouched"])

    def test_quality_rule(self):
        rule = QualityRule()
        evidence = rule.evaluate(self.context)
        self.assertEqual(evidence.identity.producer_rule, "RULE-T0-018")
        self.assertEqual(evidence.evidence_data["completeness"], 0.95)

    def test_context_alignment_rule(self):
        rule = ContextAlignmentRule()
        evidence = rule.evaluate(self.context)
        self.assertEqual(evidence.identity.producer_rule, "RULE-T0-019")
        self.assertIn("Trend", evidence.evidence_data["aligned_dimensions"])

    def test_confluence_rule(self):
        rule = ConfluenceRule()
        evidence = rule.evaluate(self.context)
        self.assertEqual(evidence.identity.producer_rule, "RULE-T0-020")
        self.assertEqual(evidence.evidence_data["number_of_confirmations"], 4)

if __name__ == "__main__":
    unittest.main()
