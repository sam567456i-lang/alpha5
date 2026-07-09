import uuid
from typing import Optional
from Backend.core.methodology.narrative_node import ExecutionPlanNode, PositionNode, ManagementNode, ExitNode
from Backend.core.methodology.narrative_types import NarrativeNodeType, NarrativeStage

class PositionLifecycleEngine:
    """
    Manages the lifecycle of a Position from creation to management to exit.
    """
    
    def open_position(self, plan: ExecutionPlanNode) -> PositionNode:
        return PositionNode(
            node_id=f"pos_{uuid.uuid4().hex[:8]}",
            identity=None,
            concept_type=NarrativeNodeType.POSITION,
            concept_name=f"Position for {plan.node_id}",
            stage=NarrativeStage.MANAGEMENT,
            plan_id=plan.node_id,
            status="OPEN",
            current_size=plan.position_size,
            average_entry_price=plan.entry_price
        )
        
    def manage_position(self, position: PositionNode, action_type: str, details: str) -> ManagementNode:
        return ManagementNode(
            node_id=f"mgmt_{uuid.uuid4().hex[:8]}",
            identity=None,
            concept_type=NarrativeNodeType.MANAGEMENT,
            concept_name=f"Management: {action_type}",
            stage=NarrativeStage.MANAGEMENT,
            position_id=position.node_id,
            action_type=action_type,
            details=details
        )
        
    def close_position(self, position: PositionNode, exit_reason: str, realized_pnl: float) -> ExitNode:
        return ExitNode(
            node_id=f"exit_{uuid.uuid4().hex[:8]}",
            identity=None,
            concept_type=NarrativeNodeType.EXIT,
            concept_name=f"Exit: {exit_reason}",
            stage=NarrativeStage.EXIT,
            position_id=position.node_id,
            exit_reason=exit_reason,
            realized_pnl=realized_pnl
        )
