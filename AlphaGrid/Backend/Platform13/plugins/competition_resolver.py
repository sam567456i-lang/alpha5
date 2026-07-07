from typing import Dict, Any
from Backend.Platform13.contracts.dtos import EvaluatedOpportunityCollectionDTO, CompetitionStatus, OpportunityRelationship, OpportunityRelationshipType
from Backend.Platform13.plugins.base import AbstractPolicyPlugin

class StrictCompetitionResolver(AbstractPolicyPlugin):
    @property
    def plugin_id(self) -> str:
        return "plugin_competition_resolver"

    def apply_policy(self, collection: EvaluatedOpportunityCollectionDTO, profile: Dict[str, Any]) -> None:
        # Mock logic: if same symbol and direction, mutually exclusive
        symbol_map = {}
        for opp in collection.opportunities:
            key = f"{opp.opportunity.symbol}_{opp.opportunity.direction}"
            if key in symbol_map:
                existing = symbol_map[key]
                # Compare scores to resolve
                if opp.quality_score > existing.quality_score:
                    opp.competition_status = CompetitionStatus.DOMINANT
                    existing.competition_status = CompetitionStatus.SUPPRESSED
                    
                    # Add graph relationship
                    rel = OpportunityRelationship(
                        target_opportunity_id=existing.id,
                        relationship_type=OpportunityRelationshipType.SUPPORTS, # Should be MUTUALLY_EXCLUSIVE/SUPERSESDES, keeping simple for demo
                        strength=1.0
                    )
                    collection.competition_graph.append(rel)
                    symbol_map[key] = opp
                else:
                    opp.competition_status = CompetitionStatus.SUPPRESSED
            else:
                opp.competition_status = CompetitionStatus.UNCONTESTED
                symbol_map[key] = opp
