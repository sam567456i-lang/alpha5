import uuid
from datetime import datetime
from typing import List, Optional

from Backend.core.analytical_rules.dto.structure.structure_state import StructureState
from Backend.core.analytical_rules.dto.structure.trend_reversal_event_dto import TrendReversalEventDTO
from Backend.core.analytical_rules.dto.structure.structural_shift_event_dto import StructuralShiftEventDTO
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.utils.identity_factory import IdentityFactory
from Backend.core.analytical_rules.capabilities.structure.shift_policy import ShiftPolicy

class StructuralShiftRule:
    """
    Consumes TrendReversalEventDTOs, StructureState, and historical breaks to emit 
    StructuralShiftEventDTOs (larger scale, confirmed transitions) based on a ShiftPolicy.
    """
    def __init__(self, policy: ShiftPolicy):
        self.policy = policy
        
    def evaluate(self, state: StructureState, reversal_event: TrendReversalEventDTO) -> List[StructuralShiftEventDTO]:
        events = []
        
        # Use the shift policy to determine if the reversal meets the persistence threshold
        historical_breaks = 1 # Simplified. In real impl, query state or history.
        current_leg_length = 1.0 # Simplified
        
        if not self.policy.is_shift(reversal_event.event_id, historical_breaks, current_leg_length):
            return events
        
        direction = reversal_event.direction
        
        geometry_fingerprint = IdentityFactory.generate_geometry_fingerprint(
            price=0.0,
            timestamp=reversal_event.event_timestamp,
            direction=direction,
            timeframe="1h",
            symbol="TEST"
        )
        
        event_id = IdentityFactory.generate_event_id("StructuralShiftEventDTO", geometry_fingerprint, self.policy.get_policy_checksum())
        
        shift_event = StructuralShiftEventDTO(
            identity=EvidenceIdentityDTO(
                evidence_id=event_id,
                evidence_type="StructuralShiftEvent",
                capability_id="CAP-STRUCTURE-05",
                ontology_id="ONT-STRUCTURE-SHIFT"
            ),
            metadata=EvidenceMetadataDTO(
                schema_version="1.0.0",
                rule_version="1.0.0",
                rule_checksum="none",
                registry_checksum="none",
                sdk_version="1.0.0",
                planner_version="1.0.0",
                fingerprint=geometry_fingerprint,
                custom_tags={}
            ),
            provenance=EvidenceProvenanceDTO(
                producer_rule="StructuralShiftRule",
                execution_mode="Standard",
                execution_timestamp=reversal_event.event_timestamp,
                source_evidence_ids=[reversal_event.event_id],
                market_dataset_id="MKT-123"
            ),
            event_id=event_id,
            event_timestamp=reversal_event.event_timestamp,
            trigger_rule="StructuralShiftRule",
            trigger_evidence=reversal_event.event_id,
            affected_state_ids=[state.state_id],
            causal_events=[{"reversal_event_id": reversal_event.event_id}],
            severity="INFO",
            sequence_number=1,
            confidence_inputs=[],
            direction=direction,
            triggering_reversal_event_id=reversal_event.event_id,
            affected_nodes=reversal_event.affected_nodes
        )
        events.append(shift_event)
        
        return events
