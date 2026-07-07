from typing import List, Dict, Any, Tuple
from Backend.Platform10.contracts.interfaces import IMethodologyPlugin
from Backend.Platform10.contracts.dtos import MarketStateDTO, ConfidenceFactorsDTO

class CompositeMethodology(IMethodologyPlugin):
    """Dynamic Composite Methodology created from multiple sub-plugins."""
    
    def __init__(self, composite_id: str, sub_plugins: List[IMethodologyPlugin]):
        self._composite_id = composite_id
        self._sub_plugins = sub_plugins
        
    @property
    def methodology_id(self) -> str:
        return self._composite_id
        
    @property
    def version(self) -> str:
        return "1.0.0"
        
    @property
    def capability_family(self) -> str:
        return "composite"
        
    def evaluate_factors(self, market_state: MarketStateDTO) -> Tuple[ConfidenceFactorsDTO, Dict[str, Any]]:
        aggregated_factors = {}
        all_supporting = []
        all_conflicting = []
        all_raw = []
        is_applicable = True
        
        for p in self._sub_plugins:
            # We don't execute full pipelines here because the sub_plugins
            # should ideally be evaluated by the MethodologyEngine first. 
            # In this simple factory, we execute them synchronously.
            factors, raw = p.evaluate_factors(market_state)
            
            for k, v in factors.factors.items():
                # Prefix the factor with the plugin ID to prevent collisions
                aggregated_factors[f"{p.methodology_id}_{k}"] = v
                
            all_supporting.extend(raw.get("supporting_concepts", []))
            all_conflicting.extend(raw.get("conflicting_concepts", []))
            all_raw.extend(raw.get("raw_evidence", []))
            if not raw.get("is_applicable", False):
                is_applicable = False
                
        return ConfidenceFactorsDTO(factors=aggregated_factors), {
            "is_applicable": is_applicable,
            "supporting_concepts": all_supporting,
            "conflicting_concepts": all_conflicting,
            "raw_evidence": all_raw,
            "required_conditions": ["Composite Components Satisfied"],
            "invalidating_conditions": ["Any Component Invalid"]
        }

class CompositeFactory:
    """Dynamically generates composite methodologies based on registry definition."""
    
    @staticmethod
    def create_composite(composite_id: str, sub_plugins: List[IMethodologyPlugin]) -> IMethodologyPlugin:
        return CompositeMethodology(composite_id, sub_plugins)
