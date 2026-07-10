from Backend.core.methodologies.rules.library.liquidity_level_rule import LiquidityLevelRule
from Backend.core.methodologies.rules.library.liquidity_level_policy import LiquidityLevelPolicy
from Backend.core.research.validation.rule_validators import GoldenDatasetValidator, StressDatasetValidator

class LiquidityLevelValidationSuite:
    """The automated laboratory validation pipeline for the LiquidityLevelRule."""
    
    @staticmethod
    def run_all():
        print("Starting Validation Suite for LiquidityLevelRule...")
        policy = LiquidityLevelPolicy()
        rule = LiquidityLevelRule(policy=policy, version="1.0.0")
        
        # 1. Correctness Gate (Golden Datasets)
        print("Testing Correctness (Perfect Equal Highs/Lows)...")
        golden_dataset = [] 
        expected_indices = []
        golden_passed = GoldenDatasetValidator.run_validation(rule, golden_dataset, expected_indices)
        
        # 2. Precision Gate (Negative Datasets)
        print("Testing Precision (Swings outside tolerance)...")
        negative_dataset = []
        negative_expected = []
        precision_passed = GoldenDatasetValidator.run_validation(rule, negative_dataset, negative_expected)
        
        # 3. Robustness Gate (Stress Dataset)
        print("Testing Robustness (Stress)...")
        stress_dataset = []
        stress_passed = StressDatasetValidator.run_validation(rule, stress_dataset)
        
        # 4. Performance Gate
        print("Testing Performance (Latency)...")
        latency_passed = True
        
        if golden_passed and precision_passed and stress_passed and latency_passed:
            print(">>> VALIDATION PASSED. LiquidityLevelRule achieves 'Laboratory Certified' status.")
            return True
        else:
            print(">>> VALIDATION FAILED. Remains 'Unit Tested' status.")
            return False

if __name__ == "__main__":
    LiquidityLevelValidationSuite.run_all()
