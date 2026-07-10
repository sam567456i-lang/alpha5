import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Backend.core.methodology.legacy_archive.ict.policies.session_policy import ICTSessionPolicy
from Backend.core.methodology.evaluators.session_evaluator import SessionEvaluator
from Backend.core.methodology.dto.base_candidate import SessionCandidate, CandidateIdentity
from test_parity_harness import ParityHarness
import datetime

def run_tests():
    # Setup legacy module
    legacy_policy = ICTSessionPolicy()
    
    def legacy_func(data):
        active_windows = data
        kz = legacy_policy.get_active_killzones(active_windows)
        sb = legacy_policy.is_silver_bullet_active(active_windows)
        # Format the output to compare
        return {"killzones": kz, "silver_bullet": sb}
        
    # Setup new evaluator
    new_evaluator = SessionEvaluator()
    
    def plat11_func(data):
        active_windows = data
        identity = CandidateIdentity(
            id=f"cand_session",
            derived_from="obj_session_1",
            policy="v1.0",
            profile="ICT",
            evaluation_id=None,
            sequence=1,
            created_at=datetime.datetime.now()
        )
        candidate = SessionCandidate(
            identity=identity,
            active_windows=active_windows
        )
        eval_result = new_evaluator.evaluate(candidate, context={})
        return {
            "killzones": eval_result.metadata["active_sessions"],
            "silver_bullet": eval_result.metadata["is_silver_bullet"]
        }

    # Test case 1: NY AM + Silver Bullet
    input_data_1 = ["08:30-12:00", "10:00-11:00"]
    ParityHarness.assert_parity(
        input_data=input_data_1,
        legacy_func=legacy_func,
        platform11_func=plat11_func
    )
    
    # Test case 3: Random window (Neither produces anything meaningful)
    input_data_3 = ["11:30-12:30"]
    ParityHarness.assert_parity(
        input_data=input_data_3,
        legacy_func=legacy_func,
        platform11_func=plat11_func
    )
    
    # Test case 4: Empty windows (Partial overlap mock for strict evaluation testing)
    input_data_4 = []
    ParityHarness.assert_parity(
        input_data=input_data_4,
        legacy_func=legacy_func,
        platform11_func=plat11_func
    )

    print("[PASS] Session Parity Test Passed")

if __name__ == "__main__":
    run_tests()
