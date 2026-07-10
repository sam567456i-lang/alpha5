from Backend.core.engine.evidence_quality import EvidenceQualityMetadata
from dataclasses import replace
import uuid
from datetime import datetime
from Backend.core.analytical_rules.dto.structure.structure_state import StructureState
from Backend.core.analytical_rules.dto.structure.swing_formation_event import SwingFormationEvent
from Backend.core.analytical_rules.dto.structure.structure_transition import StructureTransition
from Backend.core.analytical_rules.dto.structure.structure_graph_dto import StructureGraphDTO, StructureNode
from Backend.core.analytical_rules.dto.structure.structure_transition_reason import StructureTransitionReason
from Backend.core.analytical_rules.dto.structure.structure_transition_type import StructureTransitionType
from Backend.core.analytical_rules.utils.identity_factory import IdentityFactory
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

class StructureLifecycleEngine:
    """
    Consumes state and events to emit deterministic state transitions.
    Exclusively handles classification and supersession logic without observing OHLCV.
    """
    
    def apply_swing(self, state: StructureState, event: SwingFormationEvent) -> StructureTransition:
        """
        Applies a new SwingFormationEvent to the StructureState.
        Returns a StructureTransition encapsulating the old state, the event, and the new state.
        """
        # Create deep copies of the graph and identities
        new_graph_namespaces = {k: StructureGraphDTO(
            nodes=dict(g.nodes),
            edges=list(g.edges),
            active_leg_id=g.active_leg_id,
            root_node_ids=list(g.root_node_ids),
            graph_schema_version=g.graph_schema_version,
            graph_version=g.graph_version + 1,
            graph_checksum="none" # Wait to compute
        ) for k, g in state.graph_namespaces.items()}
        
        new_identities = dict(state.swing_identities)
        new_latest_highs = dict(state.latest_confirmed_high_ids)
        new_latest_lows = dict(state.latest_confirmed_low_ids)
        
        swing_id = event.swing.id
        policy_id = event.swing.policy_id
        graph_namespace = f"structure/{policy_id}"
        
        new_identities[swing_id] = event.swing
        
        if graph_namespace not in new_graph_namespaces:
            new_graph_namespaces[graph_namespace] = StructureGraphDTO()
            
        graph = new_graph_namespaces[graph_namespace]
        
        # Create a new StructureNode
        new_node = StructureNode(
            node_id=swing_id,
            node_type="NODE_STRUCTURE_SWING",
            reference_id=swing_id,
            parent_ids=[graph.active_leg_id] if graph.active_leg_id else [],
            child_ids=[],
            classification="UNCONFIRMED_INTERNAL",
            depth=1
        )
        
        # Since dataclasses are frozen, we have to recreate the graph with updated lists
        new_nodes = dict(graph.nodes)
        new_nodes[swing_id] = new_node
        
        new_root_node_ids = list(graph.root_node_ids)
        if not graph.active_leg_id:
            new_root_node_ids.append(swing_id)
            
        new_graph_namespaces[graph_namespace] = StructureGraphDTO(
            nodes=new_nodes,
            edges=graph.edges,
            active_leg_id=graph.active_leg_id,
            root_node_ids=new_root_node_ids,
            graph_schema_version=graph.graph_schema_version,
            graph_version=graph.graph_version,
            graph_checksum=graph.graph_checksum
        )
        
        if event.swing.direction == "high":
            new_latest_highs[graph_namespace] = swing_id
        elif event.swing.direction == "low":
            new_latest_lows[graph_namespace] = swing_id
            
        # Deterministic IDs
        new_evidence_id = IdentityFactory.generate_state_id(state.state_id, event.event_id)
        new_state_id = new_evidence_id # In this architecture, state_id and evidence_id are synonymous for StateEvidenceDTO
        new_transition_id = IdentityFactory.generate_transition_id(state.state_id, event.event_id)
        timestamp = event.event_timestamp

        new_state = StructureState(
            identity=EvidenceIdentityDTO(
                evidence_id=new_evidence_id, 
                evidence_type="StructureState",
                capability_id="CAP-STRUCTURE-01",
                ontology_id="ONT-STRUCTURE-STATE"
            ),
            metadata=EvidenceMetadataDTO(
                schema_version="1.0.0",
                rule_version="1.0.0",
                rule_checksum="none",
                registry_checksum="none",
                sdk_version="1.0.0",
                planner_version="1.0.0",
                fingerprint="none",
                custom_tags={}
            ),
            provenance=EvidenceProvenanceDTO(
                producer_rule="StructureLifecycleEngine",
                execution_mode="Standard",
                execution_timestamp=timestamp,
                source_evidence_ids=[state.identity.evidence_id, event.identity.evidence_id],
                market_dataset_id="MKT-123"
            ),
            classification=EvidenceClassification.COMPOSITE,
            interpretation_level=InterpretationLevel.OBJECTIVE,
            validity_status=ValidityStatus.ACTIVE,
            evidence_data={},
            quality=EvidenceQualityMetadata(confidence=1.0, coverage=1.0, freshness=0.0, latency=0.0, source_quality=1.0, sample_size=1, stability=1.0),
            state_id=new_state_id,
            created_at=timestamp,
            valid_from=event.event_timestamp,
            valid_until="null",
            is_active=True,
            invalidated_at="null",
            invalidated_by="null",
            superseded_by="null",
            related_state_ids=[],
            related_event_ids=[],
            confidence_inputs=[],
            graph_namespaces=new_graph_namespaces,
            swing_identities=new_identities,
            latest_confirmed_high_ids=new_latest_highs,
            latest_confirmed_low_ids=new_latest_lows
        )
        
        transition = StructureTransition(
            old_state=state,
            event=event,
            new_state=new_state,
            transition_id=new_transition_id,
            timestamp=timestamp,
            transition_type=StructureTransitionType.STATE_UPDATED,
            transition_reason=StructureTransitionReason.NEW_SWING
        )
        
        return transition
