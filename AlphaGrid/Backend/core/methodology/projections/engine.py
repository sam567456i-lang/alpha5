from typing import Dict, Any, List, Optional
from Backend.core.methodology.projections.dto import ProjectionDTO, ProjectionSpecification
from Backend.core.methodology.dto.base_interpretation import BaseInterpretation, SequenceInterpretation, ConfluenceInterpretation, CrossMarketInterpretation, AuctionInterpretation

class ProjectionRegistry:
    def __init__(self):
        self.specifications: Dict[str, ProjectionSpecification] = {}
        
    def register(self, spec: ProjectionSpecification):
        self.specifications[spec.name] = spec
        
    def get_specs_for_consumer(self, consumer: str) -> List[ProjectionSpecification]:
        return [spec for spec in self.specifications.values() if spec.matches_consumer(consumer)]

class ProjectionEngine:
    """
    Stateless engine that projects durable generic Interpretations into 
    methodology-branded, consumer-specific ephemeral views (ProjectionDTOs).
    """
    def __init__(self, registry: ProjectionRegistry, projection_rules: Dict[str, Any]):
        """
        projection_rules maps generic interpretations to specific brands, based on the current Profile.
        Example projection_rules:
        {
            "SequenceInterpretation": {
                "consolidation-sweep-expansion": "AMD",
                "accumulation-manipulation-distribution": "AMD"
            },
            "ConfluenceInterpretation": {
                "unicorn": "UNICORN",
                "double_fvg": "DOUBLE_FVG"
            }
        }
        """
        self.registry = registry
        self.projection_rules = projection_rules
        
    def project(self, interpretation: BaseInterpretation, consumer: str) -> List[ProjectionDTO]:
        specs = self.registry.get_specs_for_consumer(consumer)
        if not specs:
            return []
            
        projections = []
        
        # Extract base label based on interpretation type and profile rules
        base_labels = self._apply_profile_rules(interpretation)
        
        for label in base_labels:
            for spec in specs:
                # Dashboard projections might want short labels, Narrative might want sentences, etc.
                # For now, we pass the branded label to all supported specs.
                proj = ProjectionDTO(
                    projection_type=spec.name,
                    label=label,
                    consumer=consumer,
                    metadata={"original_type": type(interpretation).__name__},
                    source_interpretation_id=getattr(interpretation, "id", None)
                )
                projections.append(proj)
                
        return projections
        
    def _apply_profile_rules(self, interpretation: BaseInterpretation) -> List[str]:
        labels = []
        interp_type = type(interpretation).__name__
        rules = self.projection_rules.get(interp_type, {})
        
        if isinstance(interpretation, SequenceInterpretation):
            pattern = interpretation.sequence_pattern
            if pattern in rules:
                labels.append(rules[pattern])
            else:
                labels.append(pattern) # fallback
                
        elif isinstance(interpretation, ConfluenceInterpretation):
            pass
            
        elif isinstance(interpretation, CrossMarketInterpretation):
            div_type = interpretation.divergence_type
            if "SMT" in rules.get("divergence_labels", []):
                labels.append("SMT")
            else:
                labels.append(rules.get(div_type, "Divergence"))
                
        elif isinstance(interpretation, AuctionInterpretation):
            acc_state = interpretation.acceptance_state
            labels.append(rules.get(acc_state, f"Auction {acc_state}"))
                
        # Add Session projection etc. here.
        return labels
