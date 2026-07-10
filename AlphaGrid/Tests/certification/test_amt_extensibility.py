import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Backend.core.methodology.profiles.profile_loader import ProfileLoader
from Backend.core.methodology.evaluators.auction_evaluator import AuctionEvaluator
from Backend.core.methodology.dto.base_candidate import AuctionCandidate, CandidateIdentity
from Backend.core.methodology.dto.base_evaluation import PassedEvaluation
from Backend.core.methodology.dto.base_interpretation import AuctionInterpretation
from Backend.core.methodology.dto.interpretation_identity import InterpretationIdentity
from Backend.core.methodology.projections.engine import ProjectionRegistry, ProjectionEngine
from Backend.core.methodology.projections.dto import DashboardProjectionSpecification
from Backend.core.analytical_rules.dto.auction.auction_metrics import AuctionMetricsDTO
import datetime

def test_amt_extensibility():
    """
    Proves that Auction Market Theory (AMT) can be implemented utilizing Platform 10's
    existing auction analytical rules and Platform 11's generic evaluator.
    """
    print("Testing AMT Extensibility...")
    
    # 1. Load Profile
    loader = ProfileLoader(base_dir=os.path.join(os.path.dirname(__file__), '../../Backend/core/methodology/profiles'))
    profile_data, identity = loader.load_profile("amt_profile.yaml")
    
    auction_policy_config = profile_data.get("policies", {}).get("auction_policy", {})
    projection_rules = profile_data.get("projections", {})
    
    # 2. Init Evaluator
    evaluator = AuctionEvaluator(policy_config=auction_policy_config)
    
    registry = ProjectionRegistry()
    registry.register(DashboardProjectionSpecification())
    projection_engine = ProjectionEngine(registry, projection_rules=projection_rules)
    
    class MockMetrics:
        def __init__(self):
            self.time_inside_region = 400
            self.volume_inside_region = 1500.5
            self.rotation_count = 4
            
    p10_metrics = MockMetrics()
    
    # 4. Form Candidate
    cand_identity = CandidateIdentity(
        id="cand_amt", derived_from="metric_1", policy="v1", profile="AMT_CLASSIC",
        evaluation_id=None, sequence=1, created_at=datetime.datetime.now()
    )
    
    candidate = AuctionCandidate(
        identity=cand_identity,
        time_inside_region=p10_metrics.time_inside_region,
        volume_inside_region=p10_metrics.volume_inside_region,
        rotation_count=p10_metrics.rotation_count,
        region_type="Value Area High (VAH)"
    )
    
    # 5. Evaluate
    result = evaluator.evaluate(candidate, context={})
    assert isinstance(result, PassedEvaluation), "AMT Auction Evaluation Failed"
    
    # 6. Interpret
    interp_identity = InterpretationIdentity(
        id="interp_amt", methodology_id="amt", profile_id="classic",
        evaluation_id="eval_amt", candidate_id="cand_amt", version="1",
        hash="xyz", created=datetime.datetime.now(), sequence=1, timeframe="M5"
    )
    
    interp = AuctionInterpretation(
        identity=interp_identity,
        acceptance_state=result.metadata["acceptance_state"],
        region_type=result.metadata["region_type"],
        value_area_shift=result.metadata["value_area_shift"]
    )
    
    # 7. Project
    projections = projection_engine.project(interp, consumer="Dashboard")
    
    assert len(projections) == 1
    assert projections[0].label == "Value Area Established (Accepted)"
    
    print("[PASS] AMT Auction -> 'Value Area Established (Accepted)' correctly projected.")
    print("AMT Extensibility Proof Complete. Zero framework modifications required.")

if __name__ == "__main__":
    test_amt_extensibility()
