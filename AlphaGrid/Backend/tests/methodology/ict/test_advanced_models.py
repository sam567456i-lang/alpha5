import pytest
from Backend.core.methodology.narrative_node import (
    PDArrayNode, ConfluenceCandidateNode, SessionContextNode, 
    SessionSetupCandidateNode, StructureNarrativeNode, NarrativeNode
)
from Backend.core.methodology.narrative_types import NarrativeNodeType, NarrativeStage
from Backend.core.methodology.ict.confluence import ICTConfluenceEngine
from Backend.core.methodology.ict.session_setup import ICTSessionSetupEngine
from Backend.core.methodology.ict.sequence import ICTSequenceEngine

def test_confluence_unicorn():
    fvg = PDArrayNode(node_id="fvg_1", concept_name="FVG", array_type="FVG", concept_type=NarrativeNodeType.SETUP, stage=NarrativeStage.SETUP)
    breaker = PDArrayNode(node_id="brk_1", concept_name="Breaker", array_type="Breaker", concept_type=NarrativeNodeType.SETUP, stage=NarrativeStage.SETUP)
    cand = ConfluenceCandidateNode(node_id="cand_1", concept_name="Cand", intersecting_narrative_ids=["fvg_1", "brk_1"], concept_type=NarrativeNodeType.SETUP, stage=NarrativeStage.SETUP)
    
    engine = ICTConfluenceEngine()
    setups = engine.evaluate([cand], [fvg, breaker])
    
    assert len(setups) == 1
    assert setups[0].concept_name == "UNICORN Setup"
    
def test_session_setup_silver_bullet():
    session = SessionContextNode(node_id="sess_1", concept_name="Sess", active_time_window_ids=["10:00-11:00"], concept_type=NarrativeNodeType.SESSION_CONTEXT, stage=NarrativeStage.CONTEXT)
    struct = StructureNarrativeNode(node_id="struct_1", concept_name="Struct", structure_label="MSS", concept_type=NarrativeNodeType.STRUCTURE_NARRATIVE, stage=NarrativeStage.STRUCTURE)
    cand = SessionSetupCandidateNode(node_id="cand_1", concept_name="Cand", session_context_id="sess_1", trigger_narrative_ids=["struct_1"], concept_type=NarrativeNodeType.SETUP, stage=NarrativeStage.SETUP)
    
    engine = ICTSessionSetupEngine()
    setups = engine.evaluate([cand], [session], [struct])
    
    assert len(setups) == 1
    assert setups[0].concept_name == "SILVER_BULLET_AM Setup"
    
def test_sequence_amd():
    n1 = SessionContextNode(node_id="n1", concept_name="Asian Range", concept_type=NarrativeNodeType.SESSION_CONTEXT, stage=NarrativeStage.CONTEXT)
    n2 = StructureNarrativeNode(node_id="n2", concept_name="Liquidity Sweep", concept_type=NarrativeNodeType.STRUCTURE_NARRATIVE, stage=NarrativeStage.STRUCTURE)
    n3 = StructureNarrativeNode(node_id="n3", concept_name="MSS", concept_type=NarrativeNodeType.STRUCTURE_NARRATIVE, stage=NarrativeStage.STRUCTURE)
    n4 = NarrativeNode(node_id="n4", concept_name="OTE Entry", concept_type=NarrativeNodeType.EXECUTION, stage=NarrativeStage.EXECUTION)
    
    engine = ICTSequenceEngine()
    sequences = engine.evaluate([n1, n2, n3, n4])
    
    assert len(sequences) == 1
    assert sequences[0].concept_name == "AMD Sequence"
