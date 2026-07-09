from typing import List, Optional
from Backend.core.analytical_rules.dto.liquidity.equal_primitives import EqualHighState, EqualLowState
from Backend.core.analytical_rules.dto.liquidity.pool_events import PoolDetectedEventDTO
from Backend.core.analytical_rules.dto.liquidity.pool_identity import PoolIdentityDTO, PoolSide
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus
from Backend.core.analytical_rules.utils.identity_factory import IdentityFactory

class PoolDetectionPolicy:
    def __init__(self, 
                 minimum_anchor_count: int = 2,
                 maximum_anchor_distance: int = 10,
                 maximum_time_distance: int = 100,
                 price_buffer: float = 0.0,
                 accepted_anchor_types: List[str] = None):
        """
        Policy to govern how pools are detected from EqualStates.
        """
        self.minimum_anchor_count = minimum_anchor_count
        self.maximum_anchor_distance = maximum_anchor_distance
        self.maximum_time_distance = maximum_time_distance
        self.price_buffer = price_buffer
        self.accepted_anchor_types = accepted_anchor_types if accepted_anchor_types else ["NODE_STRUCTURE_SWING_HIGH", "NODE_STRUCTURE_SWING_LOW"]

class BuySidePoolDetector:
    """
    Consumes EqualHighState and projects a PoolDetectedEventDTO if the state meets policy.
    """
    def __init__(self, policy: PoolDetectionPolicy):
        self.policy = policy
        
    def detect(self, equal_highs: List[EqualHighState]) -> List[PoolDetectedEventDTO]:
        events = []
        for state in equal_highs:
            if state.anchor_count >= self.policy.minimum_anchor_count:
                center_price = state.average_price
                upper_bound = center_price + (state.price_variance / 2.0) + self.policy.price_buffer
                lower_bound = center_price - (state.price_variance / 2.0)
                width = upper_bound - lower_bound
                
                fingerprint = IdentityFactory.generate_geometry_fingerprint(
                    price=center_price,
                    timestamp=state.created_at,
                    direction="HIGH",
                    timeframe="unknown",
                    symbol="unknown"
                )
                
                pool_id = IdentityFactory.generate_event_id("Pool", fingerprint, "bsp_detector_v1")
                
                pool_identity = PoolIdentityDTO(
                    pool_id=pool_id,
                    pool_side=PoolSide.BUY_SIDE,
                    anchor_ids=state.anchor_ids,
                    graph_namespace="liquidity/default",
                    policy_checksum="none",
                    geometry_fingerprint=fingerprint
                )
                
                event_id = IdentityFactory.generate_event_id("PoolDetectedEventDTO", fingerprint, "bsp_detector_v1")
                
                event = PoolDetectedEventDTO(
                    identity=EvidenceIdentityDTO(
                        evidence_id=event_id,
                        evidence_type="PoolDetectedEvent",
                        capability_id="CAP-LIQUIDITY-03",
                        ontology_id="ONT-LIQUIDITY-POOL-EVENT"
                    ),
                    metadata=EvidenceMetadataDTO(
                        schema_version="1.0.0",
                        rule_version="1.0.0",
                        rule_checksum="none",
                        registry_checksum="none",
                        sdk_version="1.0.0",
                        planner_version="1.0.0",
                        fingerprint=fingerprint,
                        custom_tags={}
                    ),
                    provenance=EvidenceProvenanceDTO(
                        producer_rule="BuySidePoolDetector",
                        execution_mode="Standard",
                        execution_timestamp=state.created_at,
                        source_evidence_ids=[state.state_id],
                        market_dataset_id="MKT-123"
                    ),
                    classification=EvidenceClassification.COMPOSITE,
                    interpretation_level=InterpretationLevel.OBJECTIVE,
                    validity_status=ValidityStatus.ACTIVE,
                    evidence_data={},
                    event_id=event_id,
                    event_timestamp=state.created_at,
                    trigger_rule="BuySidePoolDetector",
                    trigger_evidence=state.state_id,
                    affected_state_ids=[],
                    causal_events=[],
                    severity="INFO",
                    sequence_number=1,
                    confidence_inputs=[state.state_id],
                    pool_identity=pool_identity,
                    center_price=center_price,
                    upper_bound=upper_bound,
                    lower_bound=lower_bound,
                    width=width,
                    anchor_distribution="UNIFORM",
                    supporting_evidence_ids=state.anchor_ids,
                    supporting_state_ids=[state.state_id],
                    policy_version="1.0.0",
                    detection_reason="Met EqualHighState threshold"
                )
                events.append(event)
                
        return events


class SellSidePoolDetector:
    """
    Consumes EqualLowState and projects a PoolDetectedEventDTO if the state meets policy.
    """
    def __init__(self, policy: PoolDetectionPolicy):
        self.policy = policy
        
    def detect(self, equal_lows: List[EqualLowState]) -> List[PoolDetectedEventDTO]:
        events = []
        for state in equal_lows:
            if state.anchor_count >= self.policy.minimum_anchor_count:
                center_price = state.average_price
                upper_bound = center_price + (state.price_variance / 2.0)
                lower_bound = center_price - (state.price_variance / 2.0) - self.policy.price_buffer
                width = upper_bound - lower_bound
                
                fingerprint = IdentityFactory.generate_geometry_fingerprint(
                    price=center_price,
                    timestamp=state.created_at,
                    direction="LOW",
                    timeframe="unknown",
                    symbol="unknown"
                )
                
                pool_id = IdentityFactory.generate_event_id("Pool", fingerprint, "ssp_detector_v1")
                
                pool_identity = PoolIdentityDTO(
                    pool_id=pool_id,
                    pool_side=PoolSide.SELL_SIDE,
                    anchor_ids=state.anchor_ids,
                    graph_namespace="liquidity/default",
                    policy_checksum="none",
                    geometry_fingerprint=fingerprint
                )
                
                event_id = IdentityFactory.generate_event_id("PoolDetectedEventDTO", fingerprint, "ssp_detector_v1")
                
                event = PoolDetectedEventDTO(
                    identity=EvidenceIdentityDTO(
                        evidence_id=event_id,
                        evidence_type="PoolDetectedEvent",
                        capability_id="CAP-LIQUIDITY-04",
                        ontology_id="ONT-LIQUIDITY-POOL-EVENT"
                    ),
                    metadata=EvidenceMetadataDTO(
                        schema_version="1.0.0",
                        rule_version="1.0.0",
                        rule_checksum="none",
                        registry_checksum="none",
                        sdk_version="1.0.0",
                        planner_version="1.0.0",
                        fingerprint=fingerprint,
                        custom_tags={}
                    ),
                    provenance=EvidenceProvenanceDTO(
                        producer_rule="SellSidePoolDetector",
                        execution_mode="Standard",
                        execution_timestamp=state.created_at,
                        source_evidence_ids=[state.state_id],
                        market_dataset_id="MKT-123"
                    ),
                    classification=EvidenceClassification.COMPOSITE,
                    interpretation_level=InterpretationLevel.OBJECTIVE,
                    validity_status=ValidityStatus.ACTIVE,
                    evidence_data={},
                    event_id=event_id,
                    event_timestamp=state.created_at,
                    trigger_rule="SellSidePoolDetector",
                    trigger_evidence=state.state_id,
                    affected_state_ids=[],
                    causal_events=[],
                    severity="INFO",
                    sequence_number=1,
                    confidence_inputs=[state.state_id],
                    pool_identity=pool_identity,
                    center_price=center_price,
                    upper_bound=upper_bound,
                    lower_bound=lower_bound,
                    width=width,
                    anchor_distribution="UNIFORM",
                    supporting_evidence_ids=state.anchor_ids,
                    supporting_state_ids=[state.state_id],
                    policy_version="1.0.0",
                    detection_reason="Met EqualLowState threshold"
                )
                events.append(event)
                
        return events
