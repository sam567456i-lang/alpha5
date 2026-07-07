from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
import uuid
import hashlib
import json
from datetime import datetime
from Backend.Platform13.contracts.dtos import EvaluatedOpportunityDTO

class RecommendationState(Enum):
    DRAFT = "DRAFT"
    GENERATED = "GENERATED"
    VALIDATED = "VALIDATED"
    APPROVED = "APPROVED"
    READY = "READY"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

@dataclass
class RecommendationDTO:
    # Core Identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    evaluated_opportunity: EvaluatedOpportunityDTO = field(default_factory=EvaluatedOpportunityDTO)
    
    # Lifecycle & Relationships
    state: RecommendationState = RecommendationState.DRAFT
    validation_errors: List[str] = field(default_factory=list)
    relationships: Dict[str, List[str]] = field(default_factory=lambda: {"supports": [], "conflicts": [], "supersedes": []})
    
    # Generated Recommendation Fields
    entry_price: Optional[float] = None
    entry_zone_min: Optional[float] = None
    entry_zone_max: Optional[float] = None
    
    stop_loss: Optional[float] = None
    take_profit_targets: List[float] = field(default_factory=list)
    
    # Trade Structure
    risk_reward_ratio: float = 0.0
    direction: str = "UNKNOWN"
    
    # Explainability & Notes
    execution_notes: List[str] = field(default_factory=list)
    confidence: float = 0.0
    
    # Data Provenance (Operational Maturity Rule 10 - Full Trace)
    producer: str = "Platform_14"
    version: str = "2.0.0"
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    registry_version: str = "1.0.0"
    
    methodology_hash: str = ""
    composite_hash: str = ""
    opportunity_hash: str = ""
    evaluation_hash: str = ""
    recommendation_hash: str = ""
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def compute_hashes(self) -> None:
        """Computes deterministic cryptographic hashes for the entire decision chain."""
        # In a real implementation, we would extract these from the nested DTOs.
        # For now, we mock the backward trace based on the evaluated_opportunity.
        if self.evaluated_opportunity and hasattr(self.evaluated_opportunity, "to_dict"):
            base_data = json.dumps(self.evaluated_opportunity.to_dict(), sort_keys=True).encode()
            self.evaluation_hash = hashlib.sha256(base_data).hexdigest()
            # Mocking the backward chain for demonstration
            self.opportunity_hash = hashlib.sha256(self.evaluation_hash.encode()).hexdigest()
            self.composite_hash = hashlib.sha256(self.opportunity_hash.encode()).hexdigest()
            self.methodology_hash = hashlib.sha256(self.composite_hash.encode()).hexdigest()
        
        output_data = json.dumps({
            "entry_price": self.entry_price,
            "stop_loss": self.stop_loss,
            "take_profit_targets": self.take_profit_targets,
            "state": self.state.value
        }, sort_keys=True)
        self.recommendation_hash = hashlib.sha256(output_data.encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "state": self.state.value,
            "evaluated_opportunity": self.evaluated_opportunity.to_dict() if hasattr(self.evaluated_opportunity, 'to_dict') else self.evaluated_opportunity,
            "entry_price": self.entry_price,
            "stop_loss": self.stop_loss,
            "take_profit_targets": self.take_profit_targets,
            "risk_reward_ratio": self.risk_reward_ratio,
            "direction": self.direction,
            "execution_notes": self.execution_notes,
            "validation_errors": self.validation_errors,
            "relationships": self.relationships,
            "confidence": self.confidence,
            "provenance": {
                "producer": self.producer,
                "version": self.version,
                "timestamp": self.timestamp,
                "registry_version": self.registry_version,
                "methodology_hash": self.methodology_hash,
                "composite_hash": self.composite_hash,
                "opportunity_hash": self.opportunity_hash,
                "evaluation_hash": self.evaluation_hash,
                "recommendation_hash": self.recommendation_hash,
                "trace_id": self.trace_id
            }
        }
