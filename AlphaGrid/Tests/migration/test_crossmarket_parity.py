import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Backend.core.methodology.legacy_archive.ict.policies.smt_policy import ICTSMTPolicy
from Backend.core.methodology.divergence_policy import DivergenceNode
from Backend.core.methodology.narrative_types import NarrativeNodeType, NarrativeStage
from Backend.core.methodology.evaluators.cross_market_evaluator import CrossMarketEvaluator
from Backend.core.methodology.dto.base_candidate import CrossMarketCandidate, CandidateIdentity
from Backend.core.methodology.dto.base_evaluation import PassedEvaluation
from Backend.core.methodology.dto.base_interpretation import CrossMarketInterpretation
from Backend.core.methodology.dto.interpretation_identity import InterpretationIdentity
from Backend.core.methodology.projections.engine import ProjectionRegistry, ProjectionEngine
from Backend.core.methodology.projections.dto import NarrativeProjectionSpecification, DashboardProjectionSpecification
from test_parity_harness import ParityHarness
import datetime

def run_tests():
    # 1. Legacy
    legacy_smt = ICTSMTPolicy()
    
    def legacy_func(data):
        div_node = DivergenceNode(
            node_id="div_1",
            identity=None,
            concept_type=NarrativeNodeType.SETUP,
            concept_name="Structural Divergence",
            stage=NarrativeStage.CONTEXT,
            primary_symbol=data["primary"],
            secondary_symbol=data["secondary"],
            divergence_type=data["div_type"],
            group_name="INDICES"
        )
        
        smt_node = legacy_smt.evaluate(div_node)
        
        if smt_node:
            # We map to the concept name for parity matching "ICT SMT Divergence"
            return {"matched_labels": [smt_node.concept_name]}
        return {"matched_labels": []}

    # 2. Plat11
    evaluator = CrossMarketEvaluator()
    registry = ProjectionRegistry()
    registry.register(DashboardProjectionSpecification())
    
    ict_profile_rules = {
        "CrossMarketInterpretation": {
            "HIGHER_HIGH_VS_LOWER_HIGH": "ICT SMT Divergence",
            "LOWER_LOW_VS_HIGHER_LOW": "ICT SMT Divergence"
        }
    }
    projection_engine = ProjectionEngine(registry, ict_profile_rules)
    
    def plat11_func(data):
        primary_state = "HIGHER_HIGH" if "HIGHER_HIGH" in data["div_type"] else ("LOWER_LOW" if "LOWER_LOW" in data["div_type"] else "NORMAL")
        sec_state = "LOWER_HIGH" if "LOWER_HIGH" in data["div_type"] else ("HIGHER_LOW" if "HIGHER_LOW" in data["div_type"] else "NORMAL")
        
        identity = CandidateIdentity(
            id="cand_cm",
            derived_from="p10_div_node",
            policy="v1",
            profile="Generic",
            evaluation_id=None,
            sequence=1,
            created_at=datetime.datetime.now()
        )
        candidate = CrossMarketCandidate(
            identity=identity,
            primary_symbol=data["primary"],
            secondary_symbol=data["secondary"],
            primary_structure_state=primary_state,
            secondary_structure_state=sec_state,
            comparison_group="INDICES"
        )
        
        result = evaluator.evaluate(candidate, context={})
        
        if isinstance(result, PassedEvaluation):
            interp_identity = InterpretationIdentity(
                id="interp_cm",
                methodology_id="generic",
                profile_id="ICT",
                evaluation_id="eval_cm",
                candidate_id="cand_cm",
                version="v1",
                hash="mock_hash",
                created=datetime.datetime.now(),
                sequence=1,
                timeframe="M5"
            )
            interp = CrossMarketInterpretation(
                identity=interp_identity,
                divergence_type=result.metadata["divergence_type"],
                primary_symbol=result.metadata["primary_symbol"],
                secondary_symbol=result.metadata["secondary_symbol"],
                bias_indication=result.metadata["bias_indication"]
            )
            
            projections = projection_engine.project(interp, consumer="Dashboard")
            configs = [p.label for p in projections]
            configs.sort()
            return {"matched_labels": configs}
        else:
            return {"matched_labels": []}

    # Test Case 1: Match SMT
    ParityHarness.assert_parity(
        input_data={"primary": "ES", "secondary": "NQ", "div_type": "HIGHER_HIGH_VS_LOWER_HIGH"},
        legacy_func=legacy_func,
        platform11_func=plat11_func
    )
    
    # Test Case 2: Rejected (No Div)
    ParityHarness.assert_parity(
        input_data={"primary": "ES", "secondary": "NQ", "div_type": "NORMAL"},
        legacy_func=legacy_func,
        platform11_func=plat11_func
    )
    
    print("[PASS] Cross-Market (SMT) Evaluation & Projection Parity Test Passed")

if __name__ == "__main__":
    run_tests()
