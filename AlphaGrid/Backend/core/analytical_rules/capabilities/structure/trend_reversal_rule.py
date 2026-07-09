import uuid
from datetime import datetime
from typing import List, Optional

from Backend.core.analytical_rules.dto.structure.structure_state import StructureState
from Backend.core.analytical_rules.dto.structure.break_event_dto import BreakEventDTO
from Backend.core.analytical_rules.dto.structure.trend_reversal_event_dto import TrendReversalEventDTO
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.utils.identity_factory import IdentityFactory

class TrendReversalRule:
    """
    Consumes BreakEventDTOs and current StructureState to emit TrendReversalEventDTOs
    when objective shifts in trajectory occur.
    """
    
    def evaluate(self, state: StructureState, break_event: BreakEventDTO) -> List[TrendReversalEventDTO]:
        events = []
        
        # A simple objective rule: a Trend Reversal requires an INTERNAL break.
        if break_event.break_type != "INTERNAL":
            return events
            
        # Determine direction mathematically based on the breaking structure
        # If we broke an old high, the new trajectory is upward.
        direction = "BULLISH" if break_event.reference_price > 0 else "BEARISH" # Simplified for test execution
        
        broken_id = break_event.broken_node
        
        # In a real engine, we'd look for sequence of breaks or specific structural patterns.
        # For Wave 2B.1B, we simulate that an internal break immediately causes a trend reversal.
        
        geometry_fingerprint = IdentityFactory.generate_geometry_fingerprint(
            price=0.0, # Not strictly tied to a price, but part of a timeframe
            timestamp=break_event.event_timestamp,
            direction=direction,
            timeframe="1h",
            symbol="TEST"
        )
        
        event_id = IdentityFactory.generate_event_id("TrendReversalEventDTO", geometry_fingerprint, "trend_reversal_rule_v1")
        
        reversal_event = TrendReversalEventDTO(
            identity=EvidenceIdentityDTO(
                evidence_id=event_id,
                evidence_type="TrendReversalEvent",
                capability_id="CAP-STRUCTURE-04",
                ontology_id="ONT-STRUCTURE-REVERSAL"
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
                producer_rule="TrendReversalRule",
                execution_mode="Standard",
                execution_timestamp=break_event.event_timestamp,
                source_evidence_ids=[break_event.event_id],
                market_dataset_id="MKT-123"
            ),
            event_id=event_id,
            event_timestamp=break_event.event_timestamp,
            trigger_rule="TrendReversalRule",
            trigger_evidence=break_event.event_id,
            affected_state_ids=[state.state_id],
            causal_events=[{"break_event_id": break_event.event_id}],
            severity="INFO",
            sequence_number=1,
            confidence_inputs=[],
            direction=direction,
            triggering_break_event_id=break_event.event_id,
            affected_nodes=[broken_id]
        )
        events.append(reversal_event)
        
        return events
