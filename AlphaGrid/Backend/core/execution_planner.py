from dataclasses import dataclass, field
from typing import List, Dict, Any
from Backend.core.interfaces.core_interfaces import ICapabilityScheduler

@dataclass(frozen=True)
class ExecutionPlan:
    """Immutable versioned execution artifact."""
    plan_id: str
    capability_order: List[str]
    dependency_graph: Dict[str, List[str]]
    configuration_hash: str
    policy_versions: Dict[str, str]
    feature_versions: Dict[str, str]
    scheduler_version: str
    planner_version: str

class ExecutionPlanner:
    """
    Compiles capabilities into a DAG and produces an ExecutionPlan.
    """
    def __init__(self, planner_version: str = "1.0"):
        self.planner_version = planner_version
        
    def build_plan(self, capabilities: List[str], deps: Dict[str, List[str]], config_hash: str) -> ExecutionPlan:
        # Simplistic topological sort stub
        ordered = list(capabilities) # assumes pre-sorted for stub
        
        return ExecutionPlan(
            plan_id="plan_001",
            capability_order=ordered,
            dependency_graph=deps,
            configuration_hash=config_hash,
            policy_versions={"ICTPolicy": "1.3"},
            feature_versions={"ATR": "1.0"},
            scheduler_version="1.0",
            planner_version=self.planner_version
        )
