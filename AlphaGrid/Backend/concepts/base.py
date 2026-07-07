"""Concept domain objects (Platform 10)."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional
from Shared.enums.concept_type import ConceptType
from Shared.dtos.execution_context import ExecutionContext

@dataclass(frozen=True)
class Concept:
    """
    Immutable semantic event representing a market concept (e.g., 'Momentum Exhaustion').
    Free-form strings are prohibited. All fields must be strictly typed.
    """
    concept_id: str
    category: str
    concept_type: ConceptType
    display_name: str
    severity: int
    priority: int
    stability: str
    status: str
    
    # 3-Layer Confidence derived from BaseObject
    deterministic_confidence: float
    statistical_confidence: float
    final_confidence: float
    
    quality: float
    expiration: Optional[datetime]
    
    execution_context: ExecutionContext
    
    # Traceability
    supporting_features: List[str] = field(default_factory=list)
    contradicting_features: List[str] = field(default_factory=list)
    consumed_states: List[str] = field(default_factory=list)
    source_ticks: List[str] = field(default_factory=list)
    
    registry_version: str = "1.0.0"
    capability_version: str = "1.0.0"
    lineage_hash: str = ""
    
    # Relationships (Metadata only, no logic execution)
    relationships_parents: List[str] = field(default_factory=list)
    relationships_children: List[str] = field(default_factory=list)
    relationships_supports: List[str] = field(default_factory=list)
    relationships_supported_by: List[str] = field(default_factory=list)
    relationships_contradicts: List[str] = field(default_factory=list)
    relationships_contradicted_by: List[str] = field(default_factory=list)
    relationships_requires: List[str] = field(default_factory=list)
    relationships_required_by: List[str] = field(default_factory=list)
    relationships_related_concepts: List[str] = field(default_factory=list)
