from typing import List, Optional
from Backend.core.analytical_rules.dto.liquidity.pool_state import PoolState
from Backend.core.analytical_rules.dto.liquidity.price_observation import PriceObservationDTO
from Backend.core.analytical_rules.dto.liquidity.pool_interaction_events import PoolInteractionEventDTO, PoolInteractionType
from Backend.core.analytical_rules.dto.liquidity.interaction_policy import InteractionPolicy
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus
from Backend.core.analytical_rules.dto.liquidity.pool_identity import PoolSide

class PoolInteractionRule:
    """
    Evaluates price observations against pool boundaries to emit objective geometric interaction events.
    Does NOT mutate PoolState.
    """
    def __init__(self, policy: InteractionPolicy = None):
        self.policy = policy or InteractionPolicy()
        
    def evaluate(self, state: PoolState, observation: PriceObservationDTO) -> Optional[PoolInteractionEventDTO]:
        if not state.active:
            return None
            
        interaction_type = None
        max_penetration = 0.0
        
        # BUY_SIDE Pool (Liquidity above current price, outer bound is lower_bound)
        if state.pool_identity.pool_side == PoolSide.BUY_SIDE:
            if observation.high > state.upper_bound:
                interaction_type = PoolInteractionType.COMPLETE_TRAVERSAL
                max_penetration = observation.high - state.lower_bound
            elif observation.high >= state.lower_bound:
                interaction_type = PoolInteractionType.ENTER
                max_penetration = observation.high - state.lower_bound
        # SELL_SIDE Pool (Liquidity below current price, outer bound is upper_bound)
        elif state.pool_identity.pool_side == PoolSide.SELL_SIDE:
            if observation.low < state.lower_bound:
                interaction_type = PoolInteractionType.COMPLETE_TRAVERSAL
                max_penetration = state.upper_bound - observation.low
            elif observation.low <= state.upper_bound:
                interaction_type = PoolInteractionType.ENTER
                max_penetration = state.upper_bound - observation.low
                
        if interaction_type:
            event_id = f"INTERACTION-{state.pool_identity.pool_id}-{observation.observation_id}"
            return PoolInteractionEventDTO(
                identity=EvidenceIdentityDTO(
                    evidence_id=event_id,
                    evidence_type="PoolInteractionEvent",
                    capability_id="CAP-LIQUIDITY-INTERACTION",
                    ontology_id="ONT-LIQUIDITY-INTERACTION-EVENT"
                ),
                metadata=EvidenceMetadataDTO(
                    schema_version="1.0.0",
                    rule_version="1.0.0",
                    rule_checksum="none",
                    registry_checksum="none",
                    sdk_version="1.0.0",
                    planner_version="1.0.0",
                    fingerprint=event_id,
                    custom_tags={}
                ),
                provenance=EvidenceProvenanceDTO(
                    producer_rule="PoolInteractionRule",
                    execution_mode="Standard",
                    execution_timestamp=observation.timestamp,
                    source_evidence_ids=[state.identity.evidence_id, observation.observation_id],
                    market_dataset_id="MKT-123"
                ),
                classification=EvidenceClassification.COMPOSITE,
                interpretation_level=InterpretationLevel.OBJECTIVE,
                validity_status=ValidityStatus.ACTIVE,
                evidence_data={},
                event_id=event_id,
                event_timestamp=observation.timestamp,
                trigger_rule="PoolInteractionRule",
                trigger_evidence=observation.observation_id,
                affected_state_ids=[],
                causal_events=[],
                severity="INFO",
                sequence_number=1,
                confidence_inputs=[],
                pool_id=state.pool_identity.pool_id,
                interaction_type=interaction_type,
                observation_id=observation.observation_id,
                entry_price=observation.open,  # Simplified for this wave
                exit_price=observation.close,  # Simplified for this wave
                maximum_penetration=max_penetration,
                duration=1,
                interaction_path="WICK" if self.policy.measurement_source == "EXTREME_PRICE" else "BODY",
                observed_price_reference=self.policy.measurement_source
            )
            
        return None
