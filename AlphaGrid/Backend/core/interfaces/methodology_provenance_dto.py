from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass(frozen=True)
class MethodologyProvenanceDTO:
    """
    Extracted metadata explicitly explaining why a methodology arrived at its state.
    Provides explainability lineages without bloating the core evaluation structure.
    """
    supporting_concepts: List[str] = field(default_factory=list)
    rejected_concepts: List[str] = field(default_factory=list)
    ignored_concepts: List[str] = field(default_factory=list)
    conflicting_concepts: List[str] = field(default_factory=list)
    graph_path: List[str] = field(default_factory=list)
    registry_versions: Dict[str, str] = field(default_factory=dict)
    evaluation_order: List[str] = field(default_factory=list)
    lineage: str = ""
    fingerprint: str = ""
