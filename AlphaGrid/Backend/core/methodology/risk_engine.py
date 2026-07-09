import uuid
from typing import Optional
from Backend.core.methodology.narrative_node import RiskNarrativeNode
from Backend.core.methodology.narrative_types import NarrativeNodeType, NarrativeStage
from Backend.core.methodology.portfolio_state import PortfolioState

class RiskEngine:
    """
    Evaluates PortfolioState to emit narrative warnings or context.
    """
    def evaluate(self, state: PortfolioState) -> Optional[RiskNarrativeNode]:
        if state.daily_realized_pnl_pct <= -state.max_daily_risk_pct:
            return RiskNarrativeNode(
                node_id=f"risk_{uuid.uuid4().hex[:8]}",
                identity=None,
                concept_type=NarrativeNodeType.RISK_NARRATIVE,
                concept_name="Daily Drawdown Exceeded",
                stage=NarrativeStage.EXECUTION,
                risk_level="CRITICAL",
                warning_message="Maximum daily risk exceeded. Trading halted."
            )
            
        if state.open_risk_pct >= state.max_open_risk_pct:
            return RiskNarrativeNode(
                node_id=f"risk_{uuid.uuid4().hex[:8]}",
                identity=None,
                concept_type=NarrativeNodeType.RISK_NARRATIVE,
                concept_name="Max Open Risk Reached",
                stage=NarrativeStage.EXECUTION,
                risk_level="WARNING",
                warning_message="Maximum open risk limit reached. New positions blocked."
            )
            
        return None
