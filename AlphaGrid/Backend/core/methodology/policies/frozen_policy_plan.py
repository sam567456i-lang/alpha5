from typing import List, Dict, Any

class FrozenPolicyPlan:
    """
    The compile-time DAG representing the execution flow for a profile.
    Runtime execution strictly follows this plan without dynamic dependency discovery.
    """
    def __init__(self, execution_order: List[str], dependencies: Dict[str, List[str]]):
        self.execution_order = execution_order
        self.dependencies = dependencies

class PolicyCompiler:
    """
    Compiles a set of declarative policies into a FrozenPolicyPlan using topological sort.
    """
    @staticmethod
    def compile(policies: List[Dict[str, Any]]) -> FrozenPolicyPlan:
        # Dummy compile logic for now
        execution_order = [p.get("id") for p in policies]
        return FrozenPolicyPlan(execution_order=execution_order, dependencies={})
