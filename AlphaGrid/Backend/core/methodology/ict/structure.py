import uuid
from typing import List, Dict, Any, Tuple
from Backend.core.methodology.multi_timeframe_graph import MultiTimeframeEvidenceGraph
from Backend.core.methodology.narrative_node import MarketContextNode, LiquidityTargetNode, StructureNarrativeNode, StructureCandidateNode
from Backend.core.methodology.narrative_types import NarrativeNodeType, MethodologyType, NarrativeStage
from Backend.core.methodology.ict.policies.structure_policy import ICTStructurePolicy

class ICTStructureModule:
    """
    Evaluates Structure Candidates based on Context, Liquidity Targets, and objective Break Events.
    Applies ICTStructurePolicy to filter Candidates into final StructureNarratives.
    """
    
    def __init__(self, policy: ICTStructurePolicy = None):
        self.policy = policy or ICTStructurePolicy()
        
    def evaluate_structure(self, mtf_graph: MultiTimeframeEvidenceGraph, context: MarketContextNode, targets: List[LiquidityTargetNode]) -> Tuple[List[StructureCandidateNode], List[StructureNarrativeNode]]:
        """
        Synthesizes objective structural breaks into Structure Candidates, then applies policies
        to emit formalized Structure Narratives.
        """
        candidates = []
        narratives = []
        
        # Mock objective breaks:
        mock_breaks = [
            {"break_id": "brk_1", "direction": "BULLISH", "type": "CONTINUATION", "tf": "15M"},
            {"break_id": "brk_2", "direction": "BEARISH", "type": "REVERSAL", "tf": "5M", "poi_mitigated": True},
            {"break_id": "brk_3", "direction": "BULLISH", "type": "REVERSAL", "tf": "1H", "swept_liquidity": True, "has_displacement": True}
        ]
        
        # 1. Generate Candidates
        for brk in mock_breaks:
            if brk["type"] == "CONTINUATION":
                cand = StructureCandidateNode(
                    node_id=f"cand_{uuid.uuid4().hex[:8]}",
                    identity=None,
                    concept_type=NarrativeNodeType.STRUCTURE_NARRATIVE,
                    concept_name=f"BOS Candidate ({brk['tf']})",
                    stage=NarrativeStage.STRUCTURE,
                    proposed_label="BOS",
                    alignment_with_context=True,
                    is_multi_timeframe_confirmed=False,
                    supporting_evidence_ids=[brk["break_id"]],
                    supporting_narrative_ids=[context.node_id],
                    producer_plugin="ICTPlugin",
                    producer_policy="v1.0"
                )
                candidates.append(cand)
                
            elif brk["type"] == "REVERSAL":
                if brk.get("swept_liquidity") and brk.get("has_displacement") and brk["tf"] in ["1H", "4H", "1D"]:
                    # MSS Candidate
                    target_refs = [t.node_id for t in targets]
                    cand = StructureCandidateNode(
                        node_id=f"cand_{uuid.uuid4().hex[:8]}",
                        identity=None,
                        concept_type=NarrativeNodeType.STRUCTURE_NARRATIVE,
                        concept_name=f"MSS Candidate ({brk['tf']})",
                        stage=NarrativeStage.STRUCTURE,
                        proposed_label="MSS",
                        alignment_with_context=True, 
                        is_multi_timeframe_confirmed=True,
                        supporting_evidence_ids=[brk["break_id"]],
                        supporting_narrative_ids=[context.node_id] + target_refs,
                        producer_plugin="ICTPlugin",
                        producer_policy="v1.0"
                    )
                    candidates.append((cand, brk)) # Store brk to pass to policy eval later if needed
                else:
                    # CHOCH Candidate
                    cand = StructureCandidateNode(
                        node_id=f"cand_{uuid.uuid4().hex[:8]}",
                        identity=None,
                        concept_type=NarrativeNodeType.STRUCTURE_NARRATIVE,
                        concept_name=f"CHOCH Candidate ({brk['tf']})",
                        stage=NarrativeStage.STRUCTURE,
                        proposed_label="CHOCH",
                        alignment_with_context=False,
                        is_multi_timeframe_confirmed=False,
                        supporting_evidence_ids=[brk["break_id"]],
                        supporting_narrative_ids=[context.node_id],
                        producer_plugin="ICTPlugin",
                        producer_policy="v1.0"
                    )
                    candidates.append((cand, brk))
                    
        # 2. Apply Policies
        final_candidates = []
        for item in candidates:
            if isinstance(item, tuple):
                cand, brk_data = item
            else:
                cand = item
                brk_data = {}
            
            final_candidates.append(cand)
            
            approved = False
            if cand.proposed_label == "BOS":
                approved = (cand.alignment_with_context == self.policy.bos.requires_context_alignment)
            elif cand.proposed_label == "CHOCH":
                mitigated = brk_data.get("poi_mitigated", False)
                if self.policy.choch.requires_poi_mitigation and mitigated:
                    approved = True
                elif not self.policy.choch.requires_poi_mitigation:
                    approved = True
            elif cand.proposed_label == "MSS":
                has_sweep = brk_data.get("swept_liquidity", False)
                has_disp = brk_data.get("has_displacement", False)
                mtf_conf = cand.is_multi_timeframe_confirmed
                
                approved = True
                if self.policy.mss.requires_htf_liquidity_sweep and not has_sweep:
                    approved = False
                if self.policy.mss.requires_displacement and not has_disp:
                    approved = False
                if self.policy.mss.requires_multi_timeframe_confirmation and not mtf_conf:
                    approved = False
                    
            if approved:
                narrative = StructureNarrativeNode(
                    node_id=f"struct_{uuid.uuid4().hex[:8]}",
                    identity=None,
                    concept_type=NarrativeNodeType.STRUCTURE_NARRATIVE,
                    concept_name=cand.concept_name.replace("Candidate", "Narrative"),
                    stage=NarrativeStage.STRUCTURE,
                    structure_label=cand.proposed_label,
                    candidate_node_id=cand.node_id,
                    supporting_narrative_ids=[cand.node_id],
                    producer_plugin="ICTPlugin",
                    producer_policy="v1.0"
                )
                narratives.append(narrative)
                
        return final_candidates, narratives
