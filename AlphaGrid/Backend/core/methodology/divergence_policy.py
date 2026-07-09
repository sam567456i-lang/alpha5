import uuid
from typing import List, Optional
from dataclasses import dataclass
from Backend.core.methodology.narrative_node import NarrativeNode
from Backend.core.methodology.narrative_types import NarrativeNodeType, NarrativeStage
from Backend.core.analytical_rules.dto.cross_market_evidence_dto import ComparisonEvidenceDTO

@dataclass(frozen=True)
class DivergenceNode(NarrativeNode):
    """Generic detection of divergence between assets in a comparison group."""
    primary_symbol: str = ""
    secondary_symbol: str = ""
    divergence_type: str = "" # e.g. "HIGHER_HIGH_VS_LOWER_HIGH"
    group_name: str = ""

class DivergencePolicy:
    """
    Consumes objective ComparisonEvidence to detect structural divergences.
    This is methodology-agnostic.
    """
    def evaluate(self, comparison: ComparisonEvidenceDTO, primary: str, secondary: str) -> Optional[DivergenceNode]:
        if comparison.comparison_type == "STRUCTURAL":
            res_primary = comparison.results.get(primary)
            res_secondary = comparison.results.get(secondary)
            
            if res_primary == "HIGHER_HIGH" and res_secondary == "LOWER_HIGH":
                return DivergenceNode(
                    node_id=f"div_{uuid.uuid4().hex[:8]}",
                    identity=None,
                    concept_type=NarrativeNodeType.SETUP,
                    concept_name="Structural Divergence",
                    stage=NarrativeStage.CONTEXT,
                    primary_symbol=primary,
                    secondary_symbol=secondary,
                    divergence_type="HIGHER_HIGH_VS_LOWER_HIGH",
                    group_name="US_INDICES" # Should come from comparison
                )
                
        return None
