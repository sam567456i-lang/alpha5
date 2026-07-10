import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Backend.core.methodology.legacy_archive.ict.confluence import ICTConfluenceEngine
from Backend.core.methodology.narrative_node import ConfluenceCandidateNode, PDArrayNode
from Backend.core.methodology.narrative_types import NarrativeNodeType, NarrativeStage
from Backend.core.methodology.evaluators.confluence_evaluator import ConfluenceEvaluator
from Backend.core.methodology.dto.base_candidate import ConfluenceCandidate, CandidateIdentity
from Backend.core.methodology.dto.base_evaluation import PassedEvaluation, RejectedEvaluation
from test_parity_harness import ParityHarness
import datetime

def run_tests():
    legacy_engine = ICTConfluenceEngine()
    
    # We use a custom configuration that is identical to the new standard we set for test
    # Legacy ICTConfluencePolicy has "UNICORN" (FVG, Breaker) and "DOUBLE_FVG" (FVG, FVG)
    
    new_evaluator = ConfluenceEvaluator()
    
    def legacy_func(data):
        # data is a dict with 'arrays' (list of types) and optionally 'archived' (list of booleans)
        arrays_types = data.get("arrays", [])
        archived = data.get("archived", [False]*len(arrays_types))
        
        arrays = []
        for i, (atype, is_arch) in enumerate(zip(arrays_types, archived)):
            # Legacy engine didn't know about archived, but we'll simulate by filtering if the new logic expects it.
            # Wait, legacy engine just matches on array type.
            # If a node was archived in legacy, it wouldn't be passed to the engine.
            if not is_arch:
                node = PDArrayNode(
                    node_id=f"pda_{i}",
                    identity=None,
                    concept_type=NarrativeNodeType.SETUP,
                    concept_name=f"{atype} Array",
                    stage=NarrativeStage.SETUP,
                    array_type=atype,
                    classification="",
                    dealing_range_node_id="dr_1",
                    supporting_evidence_ids=[],
                    supporting_narrative_ids=[],
                    producer_plugin="ICTPlugin",
                    producer_policy="v1.0"
                )
                arrays.append(node)
            
        cand = ConfluenceCandidateNode(
            node_id="cand_1",
            identity=None,
            concept_type=NarrativeNodeType.SETUP,
            concept_name="Candidate",
            stage=NarrativeStage.SETUP,
            intersecting_narrative_ids=[a.node_id for a in arrays],
            producer_plugin="ICTPlugin",
            producer_policy="v1.0"
        )
        
        setups = legacy_engine.evaluate([cand], arrays)
        
        configs = [setup.producer_policy for setup in setups]
        configs.sort()
        return {"matched_confluences": configs}
        
    def plat11_func(data):
        arrays_types = data.get("arrays", [])
        archived = data.get("archived", [False]*len(arrays_types))
        
        # Filter archived before candidate builder creates it
        valid_types = [a for a, arch in zip(arrays_types, archived) if not arch]
        
        identity = CandidateIdentity(
            id="cand_confluence",
            derived_from="pda_group",
            policy="v1",
            profile="ICT",
            evaluation_id=None,
            sequence=1,
            created_at=datetime.datetime.now()
        )
        candidate = ConfluenceCandidate(
            identity=identity,
            component_candidate_ids=[f"pda_{i}" for i in range(len(valid_types))],
            component_types=valid_types
        )
        
        result = new_evaluator.evaluate(candidate, context={})
        
        if isinstance(result, PassedEvaluation):
            configs = result.metadata["matched_profiles"]
            configs.sort()
            return {"matched_confluences": configs}
        else:
            return {"matched_confluences": []}

    # Test Case 1: Unicorn (FVG + Breaker)
    ParityHarness.assert_parity(
        input_data={"arrays": ["FVG", "Breaker", "OB"]},
        legacy_func=legacy_func,
        platform11_func=plat11_func
    )
    
    # Test Case 2: Double FVG
    ParityHarness.assert_parity(
        input_data={"arrays": ["FVG", "OB", "FVG"]},
        legacy_func=legacy_func,
        platform11_func=plat11_func
    )
    
    # Test Case 3: No Match (Wrong / Missing requirements)
    ParityHarness.assert_parity(
        input_data={"arrays": ["OB", "Breaker"]},
        legacy_func=legacy_func,
        platform11_func=plat11_func
    )
    
    # Test Case 4: Ambiguous Match (Two Unicorn candidates / FVG + FVG + Breaker)
    # This should match both UNICORN and DOUBLE_FVG
    # Legacy engine will output both: ["DOUBLE_FVG", "UNICORN"]
    ParityHarness.assert_parity(
        input_data={"arrays": ["FVG", "FVG", "Breaker"]},
        legacy_func=legacy_func,
        platform11_func=plat11_func
    )
    
    # Test Case 5: Duplicate Components (FVG, FVG, FVG, Breaker)
    # Should still match UNICORN and DOUBLE_FVG, doesn't inflate confluence.
    ParityHarness.assert_parity(
        input_data={"arrays": ["FVG", "FVG", "FVG", "Breaker"]},
        legacy_func=legacy_func,
        platform11_func=plat11_func
    )
    
    # Test Case 6: Missing Interpretation (FVG exists, Breaker archived)
    # Should reject cleanly.
    ParityHarness.assert_parity(
        input_data={
            "arrays": ["FVG", "Breaker"],
            "archived": [False, True]
        },
        legacy_func=legacy_func,
        platform11_func=plat11_func
    )

    print("[PASS] Confluence Parity Test Passed (All Edge Cases)")

if __name__ == "__main__":
    run_tests()
