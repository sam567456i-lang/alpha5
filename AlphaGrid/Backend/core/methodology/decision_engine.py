import uuid
from typing import List, Optional
from Backend.core.methodology.narrative_node import TradeSetupNode, ScoreResultNode, DecisionNode
from Backend.core.methodology.narrative_types import NarrativeNodeType, NarrativeStage

class DecisionEngine:
    """
    Evaluates setups and scores to determine whether to execute, wait, or ignore.
    """
    def __init__(self, min_score_to_execute: float = 60.0):
        self.min_score_to_execute = min_score_to_execute
        
    def evaluate(self, setup: TradeSetupNode, score_node: Optional[ScoreResultNode]) -> DecisionNode:
        if not score_node:
            decision = "WAIT"
            reason = "No score available."
        elif score_node.score >= self.min_score_to_execute:
            decision = "EXECUTE"
            reason = f"Score {score_node.score} meets execution threshold."
        elif score_node.score >= self.min_score_to_execute / 2:
            decision = "DELAY"
            reason = f"Score {score_node.score} is marginal. Waiting for further confirmation."
        else:
            decision = "IGNORE"
            reason = f"Score {score_node.score} is below actionable threshold."
            
        return DecisionNode(
            node_id=f"dec_{uuid.uuid4().hex[:8]}",
            identity=None,
            concept_type=NarrativeNodeType.DECISION,
            concept_name=f"Decision: {decision}",
            stage=NarrativeStage.EXECUTION,
            setup_id=setup.node_id,
            decision=decision,
            reasoning=reason
        )
