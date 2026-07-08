from dataclasses import dataclass, field
from typing import List, Dict, Optional
from Backend.core.interfaces.execution_mode_dto import ExecutionModeDTO

@dataclass(frozen=True)
class RuleContextDTO:
    """The immutable environment context passed to every Analytical Rule."""
    concept_references: List[str]
    methodology_context_id: str
    execution_mode: ExecutionModeDTO
    registry_versions: Dict[str, str]
    replay_metadata: Optional[Dict[str, str]] = None
    previous_evidence: List['RuleEvidenceDTO'] = field(default_factory=list)
