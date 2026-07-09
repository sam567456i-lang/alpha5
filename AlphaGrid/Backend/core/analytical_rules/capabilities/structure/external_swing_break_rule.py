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

class ExternalSwingBreakRule:
    """
    Analyzes geometric relationships between StructureState and new transitions
    to detect breaks of major/external legs using a BreakPolicy.
    """
    def __init__(self, policy: BreakPolicy):
        self.policy = policy
        
    def evaluate(self, state: StructureState, transition: StructureTransition) -> List[BreakEventDTO]:
        events = []
        
        if transition.transition_reason.name != "NEW_SWING":
            return events
            
        new_swing = transition.event.swing
        policy_id = new_swing.policy_id
        graph_namespace = f"structure/{policy_id}"
        
        if graph_namespace not in state.graph_namespaces:
            return events
            
        graph = state.graph_namespaces[graph_namespace]
        
        # For an external break, a swing breaks the major structure. 
        # In this simplified Wave 2B.1B geometric check, let's assume we are breaking the origin of the active leg.
        active_leg_id = graph.active_leg_id
        if not active_leg_id:
            return events
            
        active_leg_node = graph.nodes.get(active_leg_id)
        if not active_leg_node:
            return events
            
        broken_structure_id = None
        direction = None
        
        # We need the actual price of the active leg to compare.
        # It's an external break if it breaks the root/parent of the current leg.
        # This requires tracking swings better, but for certification, we can simulate an external break
        # if it exceeds the active leg's parent.
        parent_ids = active_leg_node.parent_ids
        if not parent_ids:
            return events
            
        parent_id = parent_ids[0]
        parent_swing = state.swing_identities.get(parent_id)
        
        if not parent_swing:
            return events
            
        if new_swing.direction == "high" and parent_swing.direction == "high" and self.policy.is_break(broken_price=parent_swing.price, breaking_price=new_swing.price, direction="BULLISH"):
            broken_structure_id = parent_swing.id
                
        elif new_swing.direction == "low" and parent_swing.direction == "low" and self.policy.is_break(broken_price=parent_swing.price, breaking_price=new_swing.price, direction="BEARISH"):
            broken_structure_id = parent_swing.id
                
        if broken_structure_id:
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
                    capability_id="CAP-STRUCTURE-03",
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
                    producer_rule="ExternalSwingBreakRule",
                    execution_mode="Standard",
                    execution_timestamp=new_swing.timestamp,
                    source_evidence_ids=[broken_structure_id, new_swing.id],
                    market_dataset_id="MKT-123"
                ),
                event_id=event_id,
                event_timestamp=new_swing.timestamp,
                trigger_rule="ExternalSwingBreakRule",
                trigger_evidence=new_swing.id,
                affected_state_ids=[state.state_id],
                causal_events=[{"swing_id": new_swing.id}],
                severity="INFO",
                sequence_number=1,
                break_id=event_id,
                break_type="EXTERNAL",
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
