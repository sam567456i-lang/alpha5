from typing import Dict, Any, List
import yaml
from Backend.Platform13.contracts.dtos import EvaluatedOpportunityDTO
from Backend.Platform14.contracts.dtos import RecommendationDTO
from Backend.Platform14.plugins.entry_generator import ZoneEntryGenerator
from Backend.Platform14.plugins.stop_generator import StructuralStopGenerator
from Backend.Platform14.plugins.target_generator import FixedRRTargetGenerator
from Backend.Platform14.plugins.structure_analyzer import TradeStructureAnalyzer
from Backend.Platform14.plugins.validator import PrePublishValidator
from Backend.Platform14.plugins.lifecycle import LifecycleEngine
from Backend.Platform14.plugins.relationship import RelationshipEngine
from Backend.Platform14.builders.recommendation_builder import RecommendationBuilder

class RecommendationGenerationPipeline:
    def __init__(self, registry_path: str):
        self.registry_path = registry_path
        self._load_registry()
        
        # Instantiate plugins
        self.entry_generator = ZoneEntryGenerator()
        self.stop_generator = StructuralStopGenerator()
        self.target_generator = FixedRRTargetGenerator()
        self.structure_analyzer = TradeStructureAnalyzer()
        
        # New Institutional Engines
        self.validator = PrePublishValidator()
        self.lifecycle = LifecycleEngine()
        self.relationship = RelationshipEngine()
        
        self.builder = RecommendationBuilder()

    def _load_registry(self):
        with open(self.registry_path, 'r') as f:
            registry = yaml.safe_load(f)
            
        for component in registry:
            if component.get("id") == "cap_platform_recommendation_generation":
                self.config = component
                self.metadata = component.get("metadata", {})
                return
        
        # If running in v2, it might be in recommendation_registry instead of flat components list
        if "recommendation_registry" in registry:
            self.metadata = registry["recommendation_registry"]
            self.policy_registry = registry.get("recommendation_policy_registry", {})
        else:
            raise ValueError("Platform 14 Registry not found")

    def _get_policy(self, policy_list_name: str, policy_id: str) -> Dict[str, Any]:
        if hasattr(self, "policy_registry"):
            policies = self.policy_registry.get(policy_list_name, [])
            for p in policies:
                if p.get("id") == policy_id:
                    return p
        else:
            policies = self.metadata.get(policy_list_name, [])
            for p in policies:
                if p.get("policy_id") == policy_id:
                    return p
        return {}

    def generate_recommendation(self, evaluated_opp: EvaluatedOpportunityDTO) -> RecommendationDTO:
        dto = RecommendationDTO(evaluated_opportunity=evaluated_opp)
        
        # Retrieve Profile (Fallback to rec_profile_standard if using old schema, else use new)
        if hasattr(self, "policy_registry"):
            profiles = self.metadata.get("profiles", [])
            profile = profiles[0] if profiles else {}
            entry_policy_id = profile.get("entry_policy", "zone_entry")
            stop_policy_id = profile.get("stop_policy", "structural_stop")
            target_policy_id = profile.get("target_policy", "fixed_target")
        else:
            profile = self.metadata.get("recommendation_profiles", [])[0]
            required_policies = profile.get("required_policies", [])
            entry_policy_id = "zone_entry" if "zone_entry" in required_policies else None
            stop_policy_id = "structural_stop" if "structural_stop" in required_policies else None
            target_policy_id = "fixed_target" if "fixed_target" in required_policies else None
            
        # 1. Generation
        if entry_policy_id:
            policy = self._get_policy("entry_policies", entry_policy_id)
            self.entry_generator.generate(dto, policy)
            
        if stop_policy_id:
            policy = self._get_policy("stop_policies", stop_policy_id)
            self.stop_generator.generate(dto, policy)
            
        if target_policy_id:
            policy = self._get_policy("target_policies", target_policy_id)
            self.target_generator.generate(dto, policy)
            
        # 2. Structure Analysis
        self.structure_analyzer.analyze(dto, {})
        
        # 3. Institutional Engines
        self.validator.analyze(dto, self._get_policy("validation_policies", profile.get("validation_policy", "strict_rr_validation")))
        self.relationship.analyze(dto, {})
        
        # Move to GENERATED -> VALIDATED -> READY
        self.lifecycle.analyze(dto, {})
        self.lifecycle.analyze(dto, {})
        
        # 4. Builder
        self.builder.build(dto, {})
        
        return dto

