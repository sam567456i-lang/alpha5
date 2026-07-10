import unittest
from Backend.core.analytical_rules.dto.rule_context_dto import RuleContextDTO
from Backend.core.interfaces.execution_mode_dto import ExecutionModeDTO
from Backend.core.analytical_rules.implementations.tier0.spatial.geometry_rule import GeometryRule
from Backend.core.analytical_rules.implementations.tier0.spatial.distance_rule import DistanceRule
from Backend.core.analytical_rules.implementations.tier0.spatial.range_rule import RangeRule
from Backend.core.analytical_rules.implementations.tier0.spatial.proximity_rule import ProximityRule

class TestSpatialRules(unittest.TestCase):
    
    def setUp(self):
        self.context = RuleContextDTO(
            concept_references=["CONCEPT-001", "CONCEPT-002"],
            methodology_context_id="CTX-001",
            execution_mode=ExecutionModeDTO(mode="Standard", description="Standard Testing"),
            registry_versions={"analytical_rule_registry": "1.0.0"}
        )

    def test_geometry_rule(self):
        rule = GeometryRule()
        evidence = rule.evaluate(self.context)
        self.assertEqual(evidence.identity.producer_rule, "RULE-T0-001")
        self.assertEqual(evidence.evidence_data["geometry_type"], "Linear")

    def test_distance_rule(self):
        rule = DistanceRule()
        evidence = rule.evaluate(self.context)
        self.assertEqual(evidence.identity.producer_rule, "RULE-T0-002")
        self.assertEqual(evidence.evidence_data["price_distance_ticks"], 50)

    def test_range_rule(self):
        rule = RangeRule()
        evidence = rule.evaluate(self.context)
        self.assertEqual(evidence.identity.producer_rule, "RULE-T0-003")
        self.assertEqual(evidence.evidence_data["price_range"], 100)
        self.assertEqual(evidence.evidence_type, "RangeEvidence")

    def test_proximity_rule(self):
        rule = ProximityRule()
        evidence = rule.evaluate(self.context)
        self.assertEqual(evidence.identity.producer_rule, "RULE-T0-004")
        self.assertTrue(evidence.evidence_data["is_overlapping"])

if __name__ == "__main__":
    unittest.main()
