import uuid
from typing import Optional
from Backend.core.methodology.narrative_node import DecisionNode, ExecutionPlanNode
from Backend.core.methodology.narrative_types import NarrativeNodeType, NarrativeStage

class ExecutionPlanner:
    """
    Translates an EXECUTE decision into a concrete ExecutionPlanNode.
    """
    def __init__(self, default_risk_pct: float = 1.0):
        self.default_risk_pct = default_risk_pct
        
    def plan(self, decision: DecisionNode, entry_price: float, stop_price: float, target_price: float) -> Optional[ExecutionPlanNode]:
        if decision.decision != "EXECUTE":
            return None
            
        # Sizing logic would interact with RiskEngine ideally, but for now we calculate a basic plan
        risk_per_share = abs(entry_price - stop_price)
        if risk_per_share == 0:
            return None # Invalid parameters
            
        return ExecutionPlanNode(
            node_id=f"plan_{uuid.uuid4().hex[:8]}",
            identity=None,
            concept_type=NarrativeNodeType.EXECUTION_PLAN,
            concept_name=f"Plan for {decision.setup_id}",
            stage=NarrativeStage.EXECUTION,
            decision_id=decision.node_id,
            entry_price=entry_price,
            stop_price=stop_price,
            target_price=target_price,
            position_size=self.default_risk_pct, # Abstracted size based on risk
            order_type="LIMIT"
        )
