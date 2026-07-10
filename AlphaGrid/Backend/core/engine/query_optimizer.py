from typing import Any, Dict, List
from dataclasses import dataclass

@dataclass
class QueryExecutionPlan:
    steps: List[str]
    estimated_cost: float

class QueryPlanner:
    """
    Database-style Query Planner for the Evidence SDK.
    Parses requests and determines optimal index routing.
    """
    def __init__(self, spatial_index: Any, temporal_index: Any):
        self.spatial_index = spatial_index
        self.temporal_index = temporal_index
        
    def plan_query(self, constraints: Dict[str, Any]) -> QueryExecutionPlan:
        steps = []
        # Extremely simplified stub logic for query cost optimization
        if "start_ms" in constraints and "end_ms" in constraints:
            steps.append("SCAN_TEMPORAL_INDEX")
        if "low_price" in constraints and "high_price" in constraints:
            steps.append("SCAN_SPATIAL_INDEX")
            
        # Re-order steps based on theoretical selectivity
        if "SCAN_TEMPORAL_INDEX" in steps and "SCAN_SPATIAL_INDEX" in steps:
            # Usually time slices are smaller than price slices in intraday
            steps = ["SCAN_TEMPORAL_INDEX", "FILTER_SPATIAL"]
            
        if not steps:
            steps = ["FULL_GRAPH_SCAN"]
            
        return QueryExecutionPlan(steps=steps, estimated_cost=100.0)
