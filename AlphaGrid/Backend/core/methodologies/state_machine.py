from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

from Backend.core.methodologies.rules.evidence import RuleEvidence
from Backend.core.methodologies.evidence import MethodologyClaim, ClaimCategory, ConfidenceVector

class LifecycleState(Enum):
    UNKNOWN = "UNKNOWN"
    # Trend
    EMERGING = "EMERGING"
    ESTABLISHED = "ESTABLISHED"
    PULLBACK = "PULLBACK"
    CONTINUATION = "CONTINUATION"
    REVERSAL = "REVERSAL"
    # SMC
    ACCUMULATION = "ACCUMULATION"
    MANIPULATION = "MANIPULATION"
    DISTRIBUTION = "DISTRIBUTION"
    MITIGATION = "MITIGATION"
    # Market Profile
    BALANCE = "BALANCE"
    INITIATIVE = "INITIATIVE"
    ACCEPTANCE = "ACCEPTANCE"
    REJECTION = "REJECTION"
    DISCOVERY = "DISCOVERY"

@dataclass(frozen=True)
class StateTransitionEvent:
    """Immutable event emitted when a methodology changes lifecycle states."""
    methodology_id: str
    instance_id: str
    timestamp: datetime
    from_state: LifecycleState
    to_state: LifecycleState
    trigger_evidence: RuleEvidence
    reason: str

class MethodologyStateMachine:
    """Explicit lifecycle tracking for methodologies."""
    def __init__(self, methodology_id: str, instance_id: str, initial_state: LifecycleState = LifecycleState.UNKNOWN):
        self.methodology_id = methodology_id
        self.instance_id = instance_id
        self.current_state = initial_state
        self.transition_history: List[StateTransitionEvent] = []
        
    def transition(self, to_state: LifecycleState, trigger: RuleEvidence, reason: str) -> StateTransitionEvent:
        event = StateTransitionEvent(
            methodology_id=self.methodology_id,
            instance_id=self.instance_id,
            timestamp=datetime.now(),
            from_state=self.current_state,
            to_state=to_state,
            trigger_evidence=trigger,
            reason=reason
        )
        self.current_state = to_state
        self.transition_history.append(event)
        return event

class EvidenceFusionEngine:
    """Fuses output from the Rule DAG into the final Methodology Claim."""
    
    @staticmethod
    def fuse_to_claim(
        claim_id: str,
        claim_type: str,
        category: ClaimCategory,
        rule_evidence_list: List[RuleEvidence],
        context_id: str,
        methodology_version: str
    ) -> MethodologyClaim:
        
        # Simple average fusion for this reference implementation
        avg_confidence = sum(e.confidence for e in rule_evidence_list) / max(1, len(rule_evidence_list))
        
        # In a real fusion engine, we compute metrics based on the provenance of the constituent rules.
        avg_direct = sum(e.provenance.direct_weight for e in rule_evidence_list) / max(1, len(rule_evidence_list))
        avg_inferred = sum(e.provenance.inferred_weight for e in rule_evidence_list) / max(1, len(rule_evidence_list))
        
        vector = ConfidenceVector(
            confidence=avg_confidence,
            data_quality=1.0,  # From context typically
            coverage=1.0,
            agreement=avg_direct,
            freshness=1.0,
            reliability=avg_inferred
        )
        
        return MethodologyClaim(
            claim_id=claim_id,
            claim_type=claim_type,
            category=category,
            confidence_vector=vector,
            valid_until_bar=10,
            invalidation_conditions=[],
            evidence_trace=[ev.rule_name for ev in rule_evidence_list],
            explanation_objects=[],
            methodology_version=methodology_version,
            context_id=context_id
        )
