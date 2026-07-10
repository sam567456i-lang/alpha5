import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Backend.core.methodology.legacy_archive.ict.liquidity import ICTLiquidityModule
from Backend.core.methodology.evaluators.liquidity_evaluator import LiquidityEvaluator
from Backend.core.methodology.dto.base_candidate import LiquidityCandidate, CandidateIdentity
from test_parity_harness import ParityHarness
import datetime

def run_tests():
    # Setup legacy module
    legacy_module = ICTLiquidityModule()
    
    def legacy_func(data):
        cands, targets = legacy_module.evaluate_targets(mtf_graph=None, context=None)
        # Return a list of tuples (pool_id, score) from the candidates sorted
        return [(c.supporting_evidence_ids[0], c.priority_score) for c in cands]
        
    # Setup new evaluator
    new_evaluator = LiquidityEvaluator()
    
    def plat11_func(data):
        # We need to supply the candidates exactly as the legacy module generated them
        raw_candidates = [
            {"pool_id": "pool_bsl_1d", "type": "BSL", "tf": "1D"},
            {"pool_id": "pool_ssl_4h", "type": "SSL", "tf": "4H"},
            {"pool_id": "pool_eqh_15m", "type": "EQH", "tf": "15M"}
        ]
        
        results = []
        for raw in raw_candidates:
            identity = CandidateIdentity(
                id=f"cand_{raw['pool_id']}",
                derived_from=raw['pool_id'],
                policy="v1.0",
                profile="ICT",
                evaluation_id=None,
                sequence=1,
                created_at=datetime.datetime.now()
            )
            candidate = LiquidityCandidate(
                identity=identity,
                metadata=raw,
                pool_id=raw["pool_id"]
            )
            eval_result = new_evaluator.evaluate(candidate, context={})
            
            # Extract score from reasons string
            reason = eval_result.reasons[0]
            score = int(reason.split("score ")[1])
            results.append((raw["pool_id"], score))
            
        # Sort results exactly as legacy module does (highest score first)
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    ParityHarness.assert_parity(
        input_data=None, # Not used in this stub
        legacy_func=legacy_func,
        platform11_func=plat11_func
    )
    print("[PASS] Liquidity Parity Test Passed")

if __name__ == "__main__":
    run_tests()
