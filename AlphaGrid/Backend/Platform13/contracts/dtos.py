from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
import uuid
from datetime import datetime
from Backend.Platform12.contracts.dtos import OpportunityDetectionDTO, OpportunityRelationship

class QueueStatus(Enum):
    CANDIDATE = "CANDIDATE"
    QUEUED = "QUEUED"
    ACTIVE = "ACTIVE"
    DOMINANT = "DOMINANT"
    WEAKENING = "WEAKENING"
    EXPIRED = "EXPIRED"
    ARCHIVED = "ARCHIVED"

class CompetitionStatus(Enum):
    UNCONTESTED = "UNCONTESTED"
    CONTESTED = "CONTESTED"
    SUPPRESSED = "SUPPRESSED"
    DOMINANT = "DOMINANT"

@dataclass
class ConfidenceProvenance:
    opportunity_score: float = 0.0
    quality_contribution: float = 0.0
    reliability_contribution: float = 0.0
    applicability_contribution: float = 0.0
    portfolio_contribution: float = 0.0
    competition_contribution: float = 0.0

@dataclass
class EvaluatedOpportunityDTO:
    # Core Identity (Wraps P12 DTO)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    opportunity: OpportunityDetectionDTO = field(default_factory=OpportunityDetectionDTO)
    
    # Metadata
    evaluation_version: str = "1.0.0"
    evaluation_trace: Dict[str, str] = field(default_factory=dict)
    
    # Scores
    composite_opportunity_score: float = 0.0
    quality_score: float = 0.0
    reliability_score: float = 0.0
    applicability_score: float = 0.0
    structural_risk_score: float = 0.0
    
    # Portfolio & Status
    portfolio_compatibility: str = "UNKNOWN"
    competition_status: CompetitionStatus = CompetitionStatus.UNCONTESTED
    queue_status: QueueStatus = QueueStatus.CANDIDATE
    
    # Provenance & Explainability
    confidence_provenance: ConfidenceProvenance = field(default_factory=ConfidenceProvenance)
    evaluation_evidence: Dict[str, Any] = field(default_factory=dict)
    evaluation_explainability: str = ""
    
    # Traceability
    derived_from: Optional[str] = None
    execution_context: Dict[str, Any] = field(default_factory=dict)
    
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "opportunity": self.opportunity.to_dict() if hasattr(self.opportunity, 'to_dict') else self.opportunity,
            "evaluation_version": self.evaluation_version,
            "evaluation_trace": self.evaluation_trace,
            "composite_opportunity_score": self.composite_opportunity_score,
            "quality_score": self.quality_score,
            "reliability_score": self.reliability_score,
            "applicability_score": self.applicability_score,
            "structural_risk_score": self.structural_risk_score,
            "portfolio_compatibility": self.portfolio_compatibility,
            "competition_status": self.competition_status.value,
            "queue_status": self.queue_status.value,
            "confidence_provenance": self.confidence_provenance.__dict__,
            "evaluation_evidence": self.evaluation_evidence,
            "evaluation_explainability": self.evaluation_explainability,
            "derived_from": self.derived_from,
            "execution_context": self.execution_context,
            "timestamp": self.timestamp
        }

@dataclass
class EvaluatedOpportunityCollectionDTO:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    ranking_metadata: Dict[str, Any] = field(default_factory=dict)
    queue_metadata: Dict[str, Any] = field(default_factory=dict)
    competition_graph: List[OpportunityRelationship] = field(default_factory=list)
    portfolio_summary: Dict[str, Any] = field(default_factory=dict)
    evaluation_statistics: Dict[str, Any] = field(default_factory=dict)
    opportunities: List[EvaluatedOpportunityDTO] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "ranking_metadata": self.ranking_metadata,
            "queue_metadata": self.queue_metadata,
            "competition_graph": [{"target": r.target_opportunity_id, "type": r.relationship_type.value, "strength": r.strength} for r in self.competition_graph],
            "portfolio_summary": self.portfolio_summary,
            "evaluation_statistics": self.evaluation_statistics,
            "opportunities": [opp.to_dict() for opp in self.opportunities],
            "timestamp": self.timestamp
        }
