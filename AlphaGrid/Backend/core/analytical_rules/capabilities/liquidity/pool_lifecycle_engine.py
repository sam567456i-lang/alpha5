from Backend.core.engine.evidence_quality import EvidenceQualityMetadata
from typing import List, Optional
from Backend.core.analytical_rules.dto.liquidity.pool_policy import PoolLifecyclePolicy
from Backend.core.analytical_rules.dto.liquidity.pool_events import PoolDetectedEventDTO
from Backend.core.analytical_rules.dto.liquidity.pool_interaction_events import PoolInteractionEventDTO, PoolInteractionType
from Backend.core.analytical_rules.dto.liquidity.pool_state import PoolState
from Backend.core.analytical_rules.dto.liquidity.pool_transitions import PoolTransition, PoolTransitionType
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

class PoolLifecycleEngine:
    """
    Pure transition executor for Liquidity Pools.
    It does not invent mutations (merges, expirations). It purely converts explicit events into explicit PoolState transitions.
    """
    def __init__(self, policy: PoolLifecyclePolicy = None):
        self.policy = policy or PoolLifecyclePolicy()
        
    def process_pool_detected_event(self, event: PoolDetectedEventDTO) -> PoolTransition:
        """
        Creates a new pool state from a detection event.
        """
        state_id = "STATE-" + event.pool_identity.pool_id
        
        new_state = PoolState(
            identity=EvidenceIdentityDTO(
                evidence_id=state_id,
                evidence_type="PoolState",
                capability_id="CAP-LIQUIDITY-LIFECYCLE",
                ontology_id="ONT-LIQUIDITY-POOL-STATE"
            ),
            metadata=EvidenceMetadataDTO(
                schema_version="1.0.0",
                rule_version="1.0.0",
                rule_checksum="none",
                registry_checksum="none",
                sdk_version="1.0.0",
                planner_version="1.0.0",
                fingerprint=event.pool_identity.geometry_fingerprint,
                custom_tags={}
            ),
            provenance=EvidenceProvenanceDTO(
                producer_rule="PoolLifecycleEngine",
                execution_mode="Standard",
                execution_timestamp=event.event_timestamp,
                source_evidence_ids=[event.event_id],
                market_dataset_id="MKT-123"
            ),
            classification=EvidenceClassification.COMPOSITE,
            interpretation_level=InterpretationLevel.OBJECTIVE,
            validity_status=ValidityStatus.ACTIVE,
            evidence_data={},
            quality=EvidenceQualityMetadata(confidence=1.0, coverage=1.0, freshness=0.0, latency=0.0, source_quality=1.0, sample_size=1, stability=1.0),
            pool_identity=event.pool_identity,
            center_price=event.center_price,
            upper_bound=event.upper_bound,
            lower_bound=event.lower_bound,
            width=event.width,
            anchor_distribution=event.anchor_distribution,
            created_by_event=event.event_id,
            created_at=event.event_timestamp,
            valid_from=event.event_timestamp,
            last_updated=event.event_timestamp,
            active=True,
            parent_pool_id=None,
            derived_pool_ids=[],
            invalidated_by=None,
            consumed_by=None,
            supporting_evidence_ids=event.supporting_evidence_ids,
            confidence_inputs=event.confidence_inputs
        )
        
        transition = PoolTransition(
            pool_id=event.pool_identity.pool_id,
            transition_type=PoolTransitionType.CREATED,
            previous_state=None,
            new_state=new_state,
            transition_reason="Pool formally created from detection event",
            trigger_event_id=event.event_id
        )
        
        return transition
        
    def process_pool_interaction_event(self, event: PoolInteractionEventDTO, current_state: PoolState) -> Optional[PoolTransition]:
        """
        Consumes a geometric interaction event and determines the lifecycle effect based on permissions.
        """
        if not current_state.active:
            return None
            
        transition_type = None
        reason = ""
        
        # A basic implementation for foundational wave. In a full system, this reads from liquidity_interaction_registry.yaml
        if event.interaction_type == PoolInteractionType.COMPLETE_TRAVERSAL:
            transition_type = PoolTransitionType.INVALIDATED
            reason = "Pool invalidated due to COMPLETE_TRAVERSAL interaction"
        elif event.interaction_type == PoolInteractionType.ENTER:
            transition_type = PoolTransitionType.UPDATED
            reason = "Pool updated due to ENTER interaction"
            
        if not transition_type:
            return None
            
        # Create new state reflecting the transition
        new_state = PoolState(
            identity=current_state.identity,
            metadata=current_state.metadata,
            provenance=EvidenceProvenanceDTO(
                producer_rule="PoolLifecycleEngine",
                execution_mode="Standard",
                execution_timestamp=event.event_timestamp,
                source_evidence_ids=[current_state.identity.evidence_id, event.event_id],
                market_dataset_id="MKT-123"
            ),
            classification=current_state.classification,
            interpretation_level=current_state.interpretation_level,
            validity_status=ValidityStatus.INVALIDATED if transition_type == PoolTransitionType.INVALIDATED else ValidityStatus.ACTIVE,
            evidence_data=current_state.evidence_data,
            quality=current_state.quality,
            pool_identity=current_state.pool_identity,
            center_price=current_state.center_price,
            upper_bound=current_state.upper_bound,
            lower_bound=current_state.lower_bound,
            width=current_state.width,
            anchor_distribution=current_state.anchor_distribution,
            created_by_event=current_state.created_by_event,
            created_at=current_state.created_at,
            valid_from=current_state.valid_from,
            last_updated=event.event_timestamp,
            active=False if transition_type == PoolTransitionType.INVALIDATED else True,
            parent_pool_id=current_state.parent_pool_id,
            derived_pool_ids=current_state.derived_pool_ids,
            superseded_by=current_state.superseded_by,
            invalidated_by=event.event_id if transition_type == PoolTransitionType.INVALIDATED else current_state.invalidated_by,
            consumed_by=current_state.consumed_by,
            supporting_evidence_ids=current_state.supporting_evidence_ids,
            confidence_inputs=current_state.confidence_inputs
        )
        
        return PoolTransition(
            pool_id=current_state.pool_identity.pool_id,
            transition_type=transition_type,
            previous_state=current_state,
            new_state=new_state,
            transition_reason=reason,
            trigger_event_id=event.event_id
        )
    
    # Future transition executors would follow this exact pattern:
    # def process_pool_merge_event(self, event: PoolMergeEventDTO, parent_states: List[PoolState]) -> PoolTransition: ...
    # def process_pool_expire_event(self, event: PoolExpireEventDTO, state: PoolState) -> PoolTransition: ...
