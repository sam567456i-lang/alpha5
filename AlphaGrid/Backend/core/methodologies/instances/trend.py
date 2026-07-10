from typing import List, Optional
from Backend.core.methodologies.core_models import MethodologyInstance, MethodologyContext
from Backend.core.methodologies.evidence import MethodologyClaim, ClaimCategory, ConfidenceVector
from Backend.core.methodologies.rules.base import DeterministicRule
from Backend.core.methodologies.rules.evidence import RuleEvidence, ProvenanceScore, ProvenanceType
from Backend.core.methodologies.state_machine import MethodologyStateMachine, LifecycleState, EvidenceFusionEngine

class TrendAlignmentRule(DeterministicRule):
    name = "TrendAlignmentRule"
    
    def evaluate(self, context: MethodologyContext) -> Optional[RuleEvidence]:
        # Extract features
        trend_strength = context.feature_snapshot.get("trend.strength.v1", 0.0)
        
        if trend_strength > 0.6:
            return RuleEvidence(
                rule_name=self.name,
                rule_version=str(self.version),
                confidence=trend_strength,
                provenance=ProvenanceScore(1.0, 0.0),
                supporting_uuids=["trend_obj_1"],
                contradicting_uuids=[]
            )
        return None

class TrendFollowingMethodology(MethodologyInstance):
    def __init__(self, instance_id, version, symbol, timeframe):
        super().__init__(instance_id, version, symbol, timeframe)
        self.state_machine = MethodologyStateMachine(version.definition.methodology_id, instance_id, LifecycleState.UNKNOWN)
        # Rule DAG
        self.trend_rule = TrendAlignmentRule()
        
    def evaluate(self, context: MethodologyContext) -> List[MethodologyClaim]:
        claims = []
        ev = self.trend_rule.evaluate(context)
        
        if ev:
            # Transition State
            self.state_machine.transition(LifecycleState.ESTABLISHED, ev, "Trend aligned")
            
            # Fuse Claim
            claim = EvidenceFusionEngine.fuse_to_claim(
                claim_id=f"clm_{self.instance_id}",
                claim_type="BullishContinuation",
                category=ClaimCategory.DIRECTIONAL,
                rule_evidence_list=[ev],
                context_id=context.context_id,
                methodology_version=self.version.version_id
            )
            claims.append(claim)
            
        return claims
