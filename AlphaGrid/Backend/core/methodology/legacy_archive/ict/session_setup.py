import uuid
from typing import List
from Backend.core.methodology.narrative_node import SessionSetupCandidateNode, TradeSetupNode, SessionContextNode, StructureNarrativeNode
from Backend.core.methodology.narrative_types import NarrativeNodeType, NarrativeStage
from Backend.core.methodology.legacy_archive.ict.policies.session_setup_policy import ICTSessionSetupPolicy

class ICTSessionSetupEngine:
    """
    Evaluates SessionSetupCandidateNodes against ICT time-based models like Silver Bullet.
    """
    def __init__(self, policy: ICTSessionSetupPolicy = None):
        self.policy = policy or ICTSessionSetupPolicy()
        
    def evaluate(self, candidates: List[SessionSetupCandidateNode], sessions: List[SessionContextNode], structures: List[StructureNarrativeNode]) -> List[TradeSetupNode]:
        setups = []
        
        session_map = {s.node_id: s for s in sessions}
        structure_map = {s.node_id: s for s in structures}
        
        for cand in candidates:
            if cand.session_context_id not in session_map:
                continue
                
            context = session_map[cand.session_context_id]
            active_windows = context.active_time_window_ids
            
            # Check if any triggers are displacements
            has_displacement = any(
                structure_map[t_id].structure_label == "MSS" or structure_map[t_id].structure_label == "CHOCH"
                for t_id in cand.trigger_narrative_ids if t_id in structure_map
            )
            
            for config in self.policy.configurations:
                # Does the active window match the configuration?
                window_match = any(req in active_windows for req in config.required_objective_windows)
                
                # Does it meet displacement requirements?
                displacement_match = (not config.requires_displacement) or has_displacement
                
                if window_match and displacement_match:
                    setup = TradeSetupNode(
                        node_id=f"ts_{uuid.uuid4().hex[:8]}",
                        identity=None,
                        concept_type=NarrativeNodeType.SETUP,
                        concept_name=f"{config.name} Setup",
                        stage=NarrativeStage.SETUP,
                        setup_direction="TBD",
                        is_active=True,
                        supporting_narrative_ids=[cand.node_id],
                        producer_plugin="ICTPlugin",
                        producer_policy=config.name
                    )
                    setups.append(setup)
                    
        return setups
