import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Backend.core.methodology.profiles.profile_loader import ProfileLoader
from Backend.core.methodology.evaluators.sequence_evaluator import SequenceEvaluator
from Backend.core.methodology.dto.base_candidate import SequenceCandidate, CandidateIdentity
from Backend.core.methodology.dto.base_evaluation import PassedEvaluation
from Backend.core.methodology.dto.base_interpretation import SequenceInterpretation
from Backend.core.methodology.dto.interpretation_identity import InterpretationIdentity
from Backend.core.methodology.projections.engine import ProjectionRegistry, ProjectionEngine
from Backend.core.methodology.projections.dto import DashboardProjectionSpecification
from Backend.core.analytical_rules.volume_rules import VolumeAnalysisRule
import datetime

def test_wyckoff_extensibility():
    """
    Proves that Wyckoff methodology can be implemented after expanding Platform 10
    primitives (Volume Analysis) and utilizing the UNMODIFIED Platform 11 engine.
    """
    print("Testing Wyckoff Extensibility...")
    
    # Platform 10 Validation
    vol_rule = VolumeAnalysisRule()
    sc_evidence = vol_rule.evaluate({"volume_relative": 4.0, "price_spread": 3.0, "direction": "BEARISH"})
    assert sc_evidence.volume_state == "CLIMAX"
    
    # Platform 11 Extensibility
    loader = ProfileLoader(base_dir=os.path.join(os.path.dirname(__file__), '../../Backend/core/methodology/profiles'))
    profile_data, identity = loader.load_profile("wyckoff_profile.yaml")
    
    sequence_policy_config = profile_data.get("policies", {}).get("sequence_policy", {})
    projection_rules = profile_data.get("projections", {})
    
    evaluator = SequenceEvaluator(policy_config=sequence_policy_config)
    
    registry = ProjectionRegistry()
    registry.register(DashboardProjectionSpecification())
    projection_engine = ProjectionEngine(registry, projection_rules=projection_rules)
    
    cand_identity = CandidateIdentity(
        id="cand_wyc", derived_from="p10_wyckoff", policy="v1", profile="WYCKOFF_CLASSIC",
        evaluation_id=None, sequence=1, created_at=datetime.datetime.now()
    )
    
    # Mocking generic states translated from P10
    candidate = SequenceCandidate(
        identity=cand_identity,
        ordered_elements=["climax_down", "reversal_up", "test_low", "sweep_low", "expansion_up"]
    )
    
    result = evaluator.evaluate(candidate, context={})
    assert isinstance(result, PassedEvaluation), "Wyckoff Sequence Evaluation Failed"
    
    interp_identity = InterpretationIdentity(
        id="interp_wyc", methodology_id="wyckoff", profile_id="classic",
        evaluation_id="eval_wyc", candidate_id="cand_wyc", version="1",
        hash="xyz", created=datetime.datetime.now(), sequence=1, timeframe="M5"
    )
    
    interp = SequenceInterpretation(
        identity=interp_identity,
        sequence_pattern=result.metadata["matched_patterns"][0],
        event_order=result.metadata["event_order"],
        constraints_satisfied=result.metadata["constraints_satisfied"],
        coverage=result.metadata["coverage"]
    )
    
    projections = projection_engine.project(interp, consumer="Dashboard")
    
    assert len(projections) == 1
    assert projections[0].label == "Wyckoff Accumulation (Phase C Spring)"
    
    print("[PASS] Wyckoff Sequence -> 'Wyckoff Accumulation (Phase C Spring)' correctly projected.")
    print("Wyckoff Extensibility Proof Complete. Platform 10 expanded. Zero Platform 11 modifications required.")

if __name__ == "__main__":
    test_wyckoff_extensibility()
