from dataclasses import dataclass, field
from typing import List
from Backend.core.methodology.narrative_types import NarrativeNodeType

@dataclass
class RequiredSequenceNode:
    concept_type: NarrativeNodeType
    concept_name_keywords: List[str] = field(default_factory=list)

@dataclass
class SequenceConfiguration:
    name: str
    required_nodes_in_order: List[RequiredSequenceNode] = field(default_factory=list)

@dataclass
class ICTSequencePolicy:
    """
    Evaluates chronological series of narrative nodes to identify advanced ICT models.
    """
    configurations: List[SequenceConfiguration] = field(default_factory=lambda: [
        SequenceConfiguration(
            name="AMD",
            required_nodes_in_order=[
                RequiredSequenceNode(concept_type=NarrativeNodeType.SESSION_CONTEXT, concept_name_keywords=["ASIAN"]),
                RequiredSequenceNode(concept_type=NarrativeNodeType.STRUCTURE_NARRATIVE, concept_name_keywords=["Sweep"]),
                RequiredSequenceNode(concept_type=NarrativeNodeType.STRUCTURE_NARRATIVE, concept_name_keywords=["MSS", "CHOCH"]),
                RequiredSequenceNode(concept_type=NarrativeNodeType.EXECUTION, concept_name_keywords=["OTE", "Entry"])
            ]
        ),
        SequenceConfiguration(
            name="JUDAS_SWING",
            required_nodes_in_order=[
                RequiredSequenceNode(concept_type=NarrativeNodeType.SESSION_CONTEXT, concept_name_keywords=["OPEN"]),
                RequiredSequenceNode(concept_type=NarrativeNodeType.STRUCTURE_NARRATIVE, concept_name_keywords=["Sweep"]),
                RequiredSequenceNode(concept_type=NarrativeNodeType.STRUCTURE_NARRATIVE, concept_name_keywords=["Reversal"])
            ]
        )
    ])
