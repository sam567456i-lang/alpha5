from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
import uuid
from datetime import datetime

class OpportunityLifecycle(Enum):
    DETECTED = "DETECTED"
    CANDIDATE = "CANDIDATE"
    CONFIRMED = "CONFIRMED"
    VALIDATED = "VALIDATED"
    WEAKENING = "WEAKENING"
    EXPIRED = "EXPIRED"
    INVALIDATED = "INVALIDATED"
    ARCHIVED = "ARCHIVED"

class OpportunityRelationshipType(Enum):
    DEPENDS_ON = "DEPENDS_ON"
    REINFORCES = "REINFORCES"
    WEAKENS = "WEAKENS"
    INVALIDATES = "INVALIDATES"
    REQUIRES = "REQUIRES"
    OPTIONAL_COMPANION = "OPTIONAL_COMPANION"
    SUPPORTS = "SUPPORTS"
    CONFLICTS = "CONFLICTS"

@dataclass
class OpportunityRelationship:
    target_opportunity_id: str
    relationship_type: OpportunityRelationshipType
    strength: float = 1.0

@dataclass
class OpportunityTrace:
    raw_tick_id: Optional[str] = None
    state_id: Optional[str] = None
    feature_ids: List[str] = field(default_factory=list)
    concept_ids: List[str] = field(default_factory=list)
    methodology_ids: List[str] = field(default_factory=list)
    composite_methodology_id: Optional[str] = None
    composite_decision_context_id: Optional[str] = None
    evaluator_id: Optional[str] = None

@dataclass
class OpportunityDetectionDTO:
    # Core Identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    opportunity_type: str = ""
    direction: str = ""
    exists: bool = False
    
    # Metadata Migrated from Legacy DTO
    market: str = ""
    symbol: str = ""
    timeframe: str = ""
    analysis_used: List[str] = field(default_factory=list)
    concepts_used: List[str] = field(default_factory=list)
    signals_used: List[str] = field(default_factory=list)
    
    # Metrics
    strength: float = 0.0
    quality: float = 0.0
    confidence: float = 0.0
    reliability: float = 0.0
    applicability: float = 0.0
    urgency: float = 0.0
    horizon: str = ""
    category: str = ""
    
    # Evidence & Context
    supporting_evidence: Dict[str, Any] = field(default_factory=dict)
    conflicting_evidence: Dict[str, Any] = field(default_factory=dict)
    opportunity_context: str = "" # Explains why now
    execution_context: Dict[str, Any] = field(default_factory=dict)
    derived_from: Optional[str] = None # Link to CompositeDecisionContextDTO
    
    # Traceability
    trace: OpportunityTrace = field(default_factory=OpportunityTrace)
    
    # Lifecycle & Relationships
    lifecycle: OpportunityLifecycle = OpportunityLifecycle.DETECTED
    relationships: List[OpportunityRelationship] = field(default_factory=list)
    
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "opportunity_type": self.opportunity_type,
            "direction": self.direction,
            "exists": self.exists,
            "market": self.market,
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "analysis_used": self.analysis_used,
            "concepts_used": self.concepts_used,
            "signals_used": self.signals_used,
            "strength": self.strength,
            "quality": self.quality,
            "confidence": self.confidence,
            "reliability": self.reliability,
            "applicability": self.applicability,
            "urgency": self.urgency,
            "horizon": self.horizon,
            "category": self.category,
            "supporting_evidence": self.supporting_evidence,
            "conflicting_evidence": self.conflicting_evidence,
            "opportunity_context": self.opportunity_context,
            "execution_context": self.execution_context,
            "derived_from": self.derived_from,
            "trace": self.trace.__dict__,
            "lifecycle": self.lifecycle.value,
            "relationships": [{"target": r.target_opportunity_id, "type": r.relationship_type.value, "strength": r.strength} for r in self.relationships],
            "timestamp": self.timestamp
        }
