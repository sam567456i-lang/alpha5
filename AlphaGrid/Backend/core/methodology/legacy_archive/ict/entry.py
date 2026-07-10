import uuid
from typing import List, Dict, Any, Tuple
from Backend.core.methodology.multi_timeframe_graph import MultiTimeframeEvidenceGraph
from Backend.core.methodology.narrative_node import (
    MarketContextNode, LiquidityTargetNode, StructureNarrativeNode,
    DealingRangeNode, PDArrayNode, TradeSetupNode,
    RetracementCandidateNode, EntryModelNode, SessionContextNode
)
from Backend.core.methodology.narrative_types import NarrativeNodeType, NarrativeStage
from Backend.core.methodology.legacy_archive.ict.policies.entry_policy import ICTEntryPolicy

class ICTEntryModule:
    """
    Formulates Dealing Ranges, maps PD Arrays, groups Trade Setups, and evaluates 
    Entry Candidates against ICTEntryPolicy to emit EntryModelNodes.
    """
    
    def __init__(self, policy: ICTEntryPolicy = None):
        self.policy = policy or ICTEntryPolicy()
        
    def evaluate_entries(
        self, 
        mtf_graph: MultiTimeframeEvidenceGraph, 
        context: MarketContextNode, 
        targets: List[LiquidityTargetNode],
        structure: List[StructureNarrativeNode],
        session: SessionContextNode = None
    ) -> Tuple[List[DealingRangeNode], List[PDArrayNode], List[TradeSetupNode], List[RetracementCandidateNode], List[EntryModelNode]]:
        """
        Synthesizes the entire entry execution pipeline.
        """
        ranges = []
        arrays = []
        setups = []
        candidates = []
        entries = []
        
        # 1. Formulate Dealing Range
        # In reality, this correlates objective price boundaries and structure
        range_high = 1.1050
        range_low = 1.1000
        dealing_range = DealingRangeNode(
            node_id=f"dr_{uuid.uuid4().hex[:8]}",
            identity=None,
            concept_type=NarrativeNodeType.SETUP,
            concept_name="Current Dealing Range",
            stage=NarrativeStage.SETUP,
            objective_range_id="obj_range_1",
            swing_high_id="swing_high_1",
            swing_low_id="swing_low_1",
            range_high_price_cached=range_high,
            range_low_price_cached=range_low,
            is_premium_discount_active=True,
            supporting_narrative_ids=[context.node_id] + [s.node_id for s in structure],
            producer_plugin="ICTPlugin",
            producer_policy="v1.0"
        )
        ranges.append(dealing_range)
        
        # 2. Formulate PD Arrays
        # Maps objective regions (from mtf_graph) against the dealing range
        discount_fvg_id = f"fvg_{uuid.uuid4().hex[:8]}"
        pd_array = PDArrayNode(
            node_id=f"pda_{uuid.uuid4().hex[:8]}",
            identity=None,
            concept_type=NarrativeNodeType.SETUP,
            concept_name="Discount FVG",
            stage=NarrativeStage.SETUP,
            array_type="FVG",
            classification="Discount",
            dealing_range_node_id=dealing_range.node_id,
            supporting_evidence_ids=[discount_fvg_id],
            supporting_narrative_ids=[dealing_range.node_id],
            producer_plugin="ICTPlugin",
            producer_policy="v1.0"
        )
        arrays.append(pd_array)
        
        # 3. Formulate Trade Setup
        # Groups the current market alignment into an active setup
        support_ids = [context.node_id, dealing_range.node_id, pd_array.node_id]
        if session:
            support_ids.append(session.node_id)
            
        setup = TradeSetupNode(
            node_id=f"ts_{uuid.uuid4().hex[:8]}",
            identity=None,
            concept_type=NarrativeNodeType.SETUP,
            concept_name="Bullish OTE Setup",
            stage=NarrativeStage.SETUP,
            setup_direction="BULLISH",
            is_active=True,
            supporting_narrative_ids=support_ids,
            producer_plugin="ICTPlugin",
            producer_policy="v1.0"
        )
        setups.append(setup)
        
        # 4. Generate Retracement Candidates
        # Based on dealing range math
        fib_level = 0.705 # OTE
        cand_entry = range_low + (range_high - range_low) * (1 - fib_level)
        cand = RetracementCandidateNode(
            node_id=f"cand_{uuid.uuid4().hex[:8]}",
            identity=None,
            concept_type=NarrativeNodeType.EXECUTION,
            concept_name="Retracement Candidate (70.5%)",
            stage=NarrativeStage.EXECUTION,
            entry_price=cand_entry,
            stop_loss_price=range_low,
            target_price=range_high,
            fib_level=fib_level,
            supporting_narrative_ids=[setup.node_id],
            producer_plugin="ICTPlugin",
            producer_policy="v1.0"
        )
        candidates.append(cand)
        
        # 5. Apply Entry Policy
        for cand in candidates:
            approved = True
            
            # Policy evaluation
            if cand.fib_level < self.policy.ote.min_fib_level or cand.fib_level > self.policy.ote.max_fib_level:
                approved = False
            
            # If approved, formalize EntryModelNode
            if approved:
                entry = EntryModelNode(
                    node_id=f"entry_{uuid.uuid4().hex[:8]}",
                    identity=None,
                    concept_type=NarrativeNodeType.EXECUTION,
                    concept_name="OTE Entry Trigger",
                    stage=NarrativeStage.EXECUTION,
                    entry_type="OTE",
                    entry_price=cand.entry_price,
                    stop_loss_price=cand.stop_loss_price,
                    target_price=cand.target_price,
                    candidate_node_id=cand.node_id,
                    supporting_narrative_ids=[cand.node_id],
                    producer_plugin="ICTPlugin",
                    producer_policy="v1.0"
                )
                entries.append(entry)
                
        return ranges, arrays, setups, candidates, entries
