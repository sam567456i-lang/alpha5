from dataclasses import dataclass, field
from typing import List, Dict

@dataclass(frozen=True)
class RuleProvenanceDTO:
    """Contains lineage and dependency mapping required for Platform 18 Explainability."""
    dependency_chain: List[str]
    parent_rules: List[str]
    supporting_concepts: List[str]
    rejected_concepts: List[str]
    graph_path: List[str]
    registry_versions: Dict[str, str] = field(default_factory=dict)
    consumed_evidence_ids: List[str] = field(default_factory=list)
    dependency_depth: int = 0
    execution_sequence: int = 0
    replay_epoch: int = 0
