import uuid
from datetime import datetime
from typing import List, Optional

from Backend.core.analytical_rules.dto.structure.structure_state import StructureState
from Backend.core.analytical_rules.dto.structure.structure_transition import StructureTransition
from Backend.core.analytical_rules.dto.structure.break_event_dto import BreakEventDTO
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.utils.identity_factory import IdentityFactory
from Backend.core.analytical_rules.capabilities.structure.break_policy import BreakPolicy

class InternalSwingBreakRule:
    """
    Analyzes geometric relationships between StructureState and new transitions
    to detect breaks of internal legs using a BreakPolicy.
    """
    def __init__(self, policy: BreakPolicy):
        self.policy = policy
        
    def evaluate(self, state: StructureState, transition: StructureTransition) -> List[BreakEventDTO]:
        events = []
        
        # We only evaluate breaks upon NEW_SWING transitions right now.
        if transition.transition_reason.name != "NEW_SWING":
            return events
            
        new_swing = transition.event.swing
        policy_id = new_swing.policy_id
        graph_namespace = f"structure/{policy_id}"
        
        if graph_namespace not in state.graph_namespaces:
            return events
            
        graph = state.graph_namespaces[graph_namespace]
        
        # An internal swing break occurs when a new swing exceeds the price of the previous opposing swing
        # However, a swing itself doesn't "break" a swing in real time; price action (candles) breaks it.
        # For Wave 2B.1B, since the engine currently only consumes SwingFormationEvents, we can simulate 
        # a break if the new swing's price exceeds the last opposing swing's price.
        # In a fully realized system, an InternalSwingBreakRule would consume candle events directly.
        
        # For this milestone, we'll implement a simplified geometric check based on the new swing.
        
        latest_high_id = state.latest_confirmed_high_ids.get(graph_namespace)
        latest_low_id = state.latest_confirmed_low_ids.get(graph_namespace)
        
        # Example logic: If the new swing is a low, check if its price is higher than the previous high? No, that's external break.
        # Internal break: Breaking the most recent internal swing.
        # Let's say if it's a high, and its price is higher than the previous high, it's a bullish break.
        # If it's a low, and its price is lower than the previous low, it's a bearish break.
        # This is a simplification for the capability verification.
        
        broken_structure_id = None
        direction = None
        
        if new_swing.direction == "high" and latest_high_id:
            last_high = state.swing_identities.get(latest_high_id)
            if last_high and self.policy.is_break(broken_price=last_high.price, breaking_price=new_swing.price, direction="BULLISH"):
                broken_structure_id = last_high.id
                
        elif new_swing.direction == "low" and latest_low_id:
            last_low = state.swing_identities.get(latest_low_id)
            if last_low and self.policy.is_break(broken_price=last_low.price, breaking_price=new_swing.price, direction="BEARISH"):
                broken_structure_id = last_low.id
                
        if broken_structure_id:
            # Generate deterministic event ID
            geometry_fingerprint = IdentityFactory.generate_geometry_fingerprint(
                price=new_swing.price,
                timestamp=new_swing.timestamp,
                direction=new_swing.direction,
                timeframe=new_swing.timeframe,
                symbol=new_swing.symbol
            )
            event_id = IdentityFactory.generate_event_id("BreakEventDTO", geometry_fingerprint, self.policy.get_policy_checksum())
            
            break_event = BreakEventDTO(
                identity=EvidenceIdentityDTO(
                    evidence_id=event_id,
                    evidence_type="BreakEvent",
                    capability_id="CAP-STRUCTURE-02",
                    ontology_id="ONT-STRUCTURE-BREAK"
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
                    producer_rule="InternalSwingBreakRule",
                    execution_mode="Standard",
                    execution_timestamp=new_swing.timestamp,
                    source_evidence_ids=[broken_structure_id, new_swing.id],
                    market_dataset_id="MKT-123"
                ),
                event_id=event_id,
                event_timestamp=new_swing.timestamp,
                trigger_rule="InternalSwingBreakRule",
                trigger_evidence=new_swing.id,
                affected_state_ids=[state.state_id],
                causal_events=[{"swing_id": new_swing.id}],
                severity="INFO",
                sequence_number=1, # simplified
                break_id=event_id,
                break_type="INTERNAL",
                broken_node=broken_structure_id,
                breaking_node=new_swing.id,
                reference_price=new_swing.price,
                reference_time=new_swing.timestamp,
                supporting_events=[new_swing.id],
                supporting_states=[state.state_id],
                confidence_inputs=[]
            )
            events.append(break_event)
            
        return events
