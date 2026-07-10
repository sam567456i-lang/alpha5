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
import datetime

def test_smc_extensibility():
    """
    Proves that the SMC methodology can be implemented purely via configuration,
    without modifying any Platform 11 engine code.
    """
    print("Testing SMC Extensibility...")
    
    # 1. Load Profile
    loader = ProfileLoader(base_dir=os.path.join(os.path.dirname(__file__), '../../Backend/core/methodology/profiles'))
    profile_data, identity = loader.load_profile("smc_profile.yaml")
    
    # 2. Extract configuration
    sequence_policy_config = profile_data.get("policies", {}).get("sequence_policy", {})
    projection_rules = profile_data.get("projections", {})
    
    # 3. Initialize UNMODIFIED Platform 11 Engines
    evaluator = SequenceEvaluator(policy_config=sequence_policy_config)
    
    registry = ProjectionRegistry()
    registry.register(DashboardProjectionSpecification())
    projection_engine = ProjectionEngine(registry, projection_rules=projection_rules)
    
    # 4. Create mock candidate simulating upstream Platform 10 SMC inputs
    # E.g., Inducement -> Expansion (CHOCH) -> Entry (Order Block Mitigated)
    cand_identity = CandidateIdentity(
        id="cand_smc", derived_from="p10", policy="v1", profile="SMC_2024",
        evaluation_id=None, sequence=1, created_at=datetime.datetime.now()
    )
    
    candidate = SequenceCandidate(
        identity=cand_identity,
        ordered_elements=["inducement", "expansion", "entry"]
    )
    
    # 5. Evaluate (Generic Sequence Evaluator)
    result = evaluator.evaluate(candidate, context={})
    assert isinstance(result, PassedEvaluation), "SMC Sequence Evaluation Failed"
    
    # 6. Form Interpretation
    interp_identity = InterpretationIdentity(
        id="interp_smc", methodology_id="smc", profile_id="2024",
        evaluation_id="eval_smc", candidate_id="cand_smc", version="1",
        hash="xyz", created=datetime.datetime.now(), sequence=1, timeframe="M5"
    )
    
    interp = SequenceInterpretation(
        identity=interp_identity,
        sequence_pattern=result.metadata["matched_patterns"][0],
        event_order=result.metadata["event_order"],
        constraints_satisfied=result.metadata["constraints_satisfied"],
        coverage=result.metadata["coverage"]
    )
    
    # 7. Project (Stateless Projection Engine)
    projections = projection_engine.project(interp, consumer="Dashboard")
    
    assert len(projections) == 1
    assert projections[0].label == "SMC Liquidity Inducement Setup"
    
    print("[PASS] SMC Sequence -> 'SMC Liquidity Inducement Setup' correctly projected.")
    print("SMC Extensibility Proof Complete. Zero framework modifications required.")

if __name__ == "__main__":
    test_smc_extensibility()
