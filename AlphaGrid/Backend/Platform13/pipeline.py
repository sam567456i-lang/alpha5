from typing import List, Dict, Any
from Backend.Platform12.contracts.dtos import OpportunityDetectionDTO
from Backend.Platform13.contracts.dtos import EvaluatedOpportunityDTO, EvaluatedOpportunityCollectionDTO
from Backend.Platform13.plugins.base import AbstractAssessmentPlugin, AbstractPolicyPlugin, AbstractBuilderPlugin, AbstractRankingPlugin, AbstractLifecyclePlugin

class OpportunityEvaluationPipeline:
    def __init__(self, plugins: Dict[str, Any], registry_config: Dict[str, Any]):
        self.plugins = plugins
        self.registry_config = registry_config
        self.evaluation_profiles = self.registry_config.get("evaluation_profiles", [])
        self.scoring_policies = {p["policy_id"]: p for p in self.registry_config.get("scoring_policies", [])}
        self.competition_policies = {p["policy_id"]: p for p in self.registry_config.get("competition_policies", [])}
        self.queue_policies = {p["policy_id"]: p for p in self.registry_config.get("queue_policies", [])}
        
    def execute(self, opportunities: List[OpportunityDetectionDTO]) -> EvaluatedOpportunityCollectionDTO:
        collection = EvaluatedOpportunityCollectionDTO()
        
        # 0. Wrap incoming
        for opp in opportunities:
            eval_opp = EvaluatedOpportunityDTO(opportunity=opp)
            eval_opp.derived_from = opp.id
            collection.opportunities.append(eval_opp)
            
        profile = self.evaluation_profiles[0] if self.evaluation_profiles else {}
        
        # 1. Assessment
        for opp in collection.opportunities:
            for assessor in self.plugins.get("assessors", []):
                assessor.assess(opp, profile)
                
        # 2. Builder (Scoring)
        scoring_policy = self.scoring_policies.get("standard_scoring", {})
        for opp in collection.opportunities:
            for builder in self.plugins.get("builders", []):
                builder.build(opp, scoring_policy)
                
        # 3. Policy (Competition)
        comp_policy = self.competition_policies.get("strict_competition", {})
        for policy_plugin in self.plugins.get("policies", []):
            policy_plugin.apply_policy(collection, comp_policy)
            
        # 4. Lifecycle (Queue)
        queue_policy = self.queue_policies.get("standard_queue", {})
        for opp in collection.opportunities:
            for lifecycle in self.plugins.get("lifecycles", []):
                lifecycle.manage_lifecycle(opp, queue_policy)
                
        # 5. Ranking (Mock simple ranking)
        collection.opportunities.sort(key=lambda x: x.composite_opportunity_score, reverse=True)
        
        return collection
