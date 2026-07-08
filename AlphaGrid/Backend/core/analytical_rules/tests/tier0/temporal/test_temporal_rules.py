import unittest
from Backend.core.analytical_rules.dto.rule_context_dto import RuleContextDTO
from Backend.core.interfaces.execution_mode_dto import ExecutionModeDTO
from Backend.core.analytical_rules.implementations.tier0.temporal.time_rule import TimeRule
from Backend.core.analytical_rules.implementations.tier0.temporal.session_rule import SessionRule
from Backend.core.analytical_rules.implementations.tier0.temporal.calendar_rule import CalendarRule
from Backend.core.analytical_rules.implementations.tier0.temporal.multi_timeframe_rule import MultiTimeframeRule

class TestTemporalRules(unittest.TestCase):
    
    def setUp(self):
        self.context = RuleContextDTO(
            concept_references=["CONCEPT-T-001", "CONCEPT-T-002"],
            methodology_context_id="CTX-002",
            execution_mode=ExecutionModeDTO(mode="Standard", description="Standard Testing"),
            registry_versions={"analytical_rule_registry": "1.0.0"}
        )

    def test_time_rule(self):
        rule = TimeRule()
        evidence = rule.evaluate(self.context)
        self.assertEqual(evidence.identity.producer_rule, "RULE-T0-005")
        self.assertTrue(evidence.evidence_data["is_market_open"])
        self.assertEqual(evidence.evidence_type, "TimeEvidence")

    def test_session_rule(self):
        rule = SessionRule()
        evidence = rule.evaluate(self.context)
        self.assertEqual(evidence.identity.producer_rule, "RULE-T0-006")
        self.assertEqual(evidence.evidence_data["current_session"], "NY")
        self.assertEqual(evidence.evidence_type, "SessionEvidence")

    def test_calendar_rule(self):
        rule = CalendarRule()
        evidence = rule.evaluate(self.context)
        self.assertEqual(evidence.identity.producer_rule, "RULE-T0-007")
        self.assertEqual(evidence.evidence_data["is_holiday"], False)
        self.assertEqual(evidence.evidence_type, "CalendarEvidence")

    def test_multi_timeframe_rule(self):
        rule = MultiTimeframeRule()
        evidence = rule.evaluate(self.context)
        self.assertEqual(evidence.identity.producer_rule, "RULE-T0-008")
        self.assertTrue(evidence.evidence_data["is_aligned"])

if __name__ == "__main__":
    unittest.main()
