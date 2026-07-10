from typing import List, Dict, Any
from Backend.core.methodology.dto.base_interpretation import BaseInterpretation

class BaseProjection:
    """
    Stateless view mapper from InterpretationGraph to a specific format.
    """
    def project(self, interpretations: List[BaseInterpretation]) -> Any:
        raise NotImplementedError()

class NarrativeProjection(BaseProjection):
    """
    Maps interpretations into a human-readable narrative string or object.
    Does not modify the InterpretationGraph.
    """
    def project(self, interpretations: List[BaseInterpretation]) -> str:
        narrative_parts = []
        for interp in interpretations:
            if hasattr(interp, 'narrative_text') and interp.narrative_text:
                narrative_parts.append(interp.narrative_text)
            elif hasattr(interp, 'bias_direction') and interp.bias_direction:
                narrative_parts.append(f"Bias is {interp.bias_direction}.")
            elif hasattr(interp, 'structure_type') and interp.structure_type:
                narrative_parts.append(f"Structure is {interp.structure_type}.")
                
        return " ".join(narrative_parts) if narrative_parts else "No narrative available."

class ProjectionEngine:
    """
    Stateless engine to generate views (Projections) from the InterpretationGraph.
    """
    def __init__(self):
        self.projections: Dict[str, BaseProjection] = {
            "narrative": NarrativeProjection()
            # other projections: dashboard, report, llm, decision
        }
        
    def generate_projection(self, projection_type: str, interpretations: List[BaseInterpretation]) -> Any:
        proj = self.projections.get(projection_type)
        if not proj:
            raise ValueError(f"Projection type {projection_type} not found.")
        return proj.project(interpretations)
