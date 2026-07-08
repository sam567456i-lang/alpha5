import unittest
from Backend.core.analytical_rules.planner.rule_planner import RuleExecutionPlanner
from Backend.core.analytical_rules.graph.rule_graph import RuleDependencyGraph
from Backend.core.analytical_rules.dto.rule_context_dto import RuleContextDTO
from Backend.core.interfaces.execution_mode_dto import ExecutionModeDTO

class MockRule:
    def __init__(self, rule_id, dependencies):
        self.rule_id = rule_id
        self.dependencies = dependencies
    def get_capabilities(self):
        return {"capability_id": self.rule_id}
    def get_dependencies(self):
        return self.dependencies

class TestTier0Planner(unittest.TestCase):
    
    def setUp(self):
        self.planner = RuleExecutionPlanner()
        self.context = RuleContextDTO(
            concept_references=[],
            methodology_context_id="TEST",
            execution_mode=ExecutionModeDTO(mode="Standard", description=""),
            registry_versions={}
        )

    def test_planner_topological_batching(self):
        graph = RuleDependencyGraph()
        # A depends on nothing
        graph.add_rule("A", [])
        # B depends on A
        graph.add_rule("B", ["A"])
        # C depends on A
        graph.add_rule("C", ["A"])
        # D depends on B and C
        graph.add_rule("D", ["B", "C"])
        
        plan = self.planner.plan_execution(graph, self.context)
        
        self.assertTrue(graph.validate_dag())
        self.assertEqual(len(plan.execution_batches), 3)
        self.assertEqual(plan.execution_batches[0], ["A"])
        self.assertCountEqual(plan.execution_batches[1], ["B", "C"])
        self.assertEqual(plan.execution_batches[2], ["D"])

    def test_blocked_rule_propagation(self):
        graph = RuleDependencyGraph()
        graph.add_rule("A", [])
        graph.add_rule("B", ["A"])
        graph.add_rule("C", ["A"])
        graph.add_rule("D", ["B", "C"])
        
        # Block 'B'
        plan = self.planner.plan_execution(graph, self.context, blocked_rules=["B"])
        
        # A dependency is blocked, so D should be skipped.
        self.assertIn("D", plan.skipped_rules)
        self.assertNotIn("C", plan.skipped_rules)

if __name__ == "__main__":
    unittest.main()
