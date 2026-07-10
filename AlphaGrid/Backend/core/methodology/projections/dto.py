from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from Backend.core.methodology.dto.base_interpretation import BaseInterpretation

@dataclass(frozen=True)
class ProjectionDTO:
    """
    Transient, stateless view representing a methodology-specific or consumer-specific 
    presentation of an Interpretation. Never stored in the permanent graph.
    """
    projection_type: str
    label: str
    consumer: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    source_interpretation_id: Optional[str] = None

class ProjectionSpecification:
    """
    Defines capabilities and requirements for a specific type of projection view.
    """
    def __init__(self, name: str, supports: List[str]):
        self.name = name
        self.supports = supports
        
    def matches_consumer(self, consumer: str) -> bool:
        return consumer in self.supports

class NarrativeProjectionSpecification(ProjectionSpecification):
    def __init__(self):
        super().__init__("NarrativeProjection", ["Narrative", "LLM", "Report"])

class DashboardProjectionSpecification(ProjectionSpecification):
    def __init__(self):
        super().__init__("DashboardProjection", ["Dashboard", "UI"])
