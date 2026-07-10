import uuid
from typing import Optional
from dataclasses import dataclass
from Backend.core.methodology.narrative_node import NarrativeNode
from Backend.core.methodology.divergence_policy import DivergenceNode
from Backend.core.methodology.narrative_types import NarrativeNodeType, NarrativeStage

@dataclass(frozen=True)
class SMTNarrativeNode(NarrativeNode):
    """ICT Smart Money Technique divergence interpretation."""
    primary_symbol: str = ""
    diverging_symbol: str = ""
    bias_indication: str = "" # BULLISH, BEARISH

class ICTSMTPolicy:
    """
    Interprets raw objective divergences into ICT Smart Money Technique narratives.
    """
    def evaluate(self, divergence: DivergenceNode) -> Optional[SMTNarrativeNode]:
        if divergence.divergence_type == "HIGHER_HIGH_VS_LOWER_HIGH":
            # Just a stub logic: if primary made HH and secondary didn't, it implies strength in primary
            return SMTNarrativeNode(
                node_id=f"smt_{uuid.uuid4().hex[:8]}",
                identity=None,
                concept_type=NarrativeNodeType.MARKET_CONTEXT,
                concept_name="ICT SMT Divergence",
                stage=NarrativeStage.CONTEXT,
                primary_symbol=divergence.primary_symbol,
                diverging_symbol=divergence.secondary_symbol,
                bias_indication="BULLISH"
            )
            
        return None
