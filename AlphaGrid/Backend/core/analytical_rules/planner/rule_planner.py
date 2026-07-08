from Backend.core.analytical_rules.dto.rule_execution_plan_dto import RuleExecutionPlanDTO
from Backend.core.analytical_rules.graph.rule_graph import RuleDependencyGraph
from Backend.core.analytical_rules.dto.rule_context_dto import RuleContextDTO
from typing import List, Dict

class RuleExecutionPlanner:
    """
    Determines execution batches, skip paths, and replay scheduling from the RuleDependencyGraph.
    Passes the deterministic RuleExecutionPlanDTO to the RuleRuntime.
    """
    def plan_execution(self, graph: RuleDependencyGraph, context: RuleContextDTO, blocked_rules: List[str] = None) -> RuleExecutionPlanDTO:
        if blocked_rules is None:
            blocked_rules = []
            
        ordered_rules = graph.get_topological_order()
        
        execution_batches = []
        in_degree = {u: 0 for u in ordered_rules}
        for u in ordered_rules:
            for v in graph.graph.successors(u):
                if v in in_degree:
                    in_degree[v] += 1
                    
        zero_in_degree = [u for u, d in in_degree.items() if d == 0]
        
        while zero_in_degree:
            # Sort for deterministic execution plans
            zero_in_degree.sort()
            execution_batches.append(zero_in_degree)
            next_zero = []
            for u in zero_in_degree:
                for v in graph.graph.successors(u):
                    if v in in_degree:
                        in_degree[v] -= 1
                        if in_degree[v] == 0:
                            next_zero.append(v)
            zero_in_degree = next_zero
            
        # Determine skipped/blocked propagation
        skipped_rules = set()
        for rule in ordered_rules:
            deps = graph.get_dependencies(rule)
            if any(dep in blocked_rules or dep in skipped_rules for dep in deps):
                skipped_rules.add(rule)
                
        # The dependency map representation for DTO
        dependency_map = {n: graph.get_dependencies(n) for n in ordered_rules}

        return RuleExecutionPlanDTO(
            ordered_rules=ordered_rules,
            dependency_graph=dependency_map,
            execution_batches=execution_batches,
            replay_metadata={"epoch": 0, "mode": context.execution_mode.mode if context.execution_mode else "Standard"},
            skipped_rules=list(skipped_rules)
        )
