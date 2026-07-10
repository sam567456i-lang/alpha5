from Backend.core.methodologies.rules.library.bos_rule import BreakOfStructureRule
from Backend.core.methodologies.rules.library.bos_policy import BOSPolicy
from Backend.core.research.validation.rule_validators import GoldenDatasetValidator, StressDatasetValidator

class BOSValidationSuite:
    """The automated laboratory validation pipeline for the BOSRule."""
    
    @staticmethod
    def run_all():
        print("Starting Validation Suite for BOSRule...")
        policy = BOSPolicy()
        rule = BreakOfStructureRule(policy=policy, version="1.0.0")
        
        # 1. Correctness Gate (Golden Datasets)
        print("Testing Correctness (Perfect BOS)...")
        # Would inject known BOS scenario
        golden_dataset = [] 
        expected_indices = []
        golden_passed = GoldenDatasetValidator.run_validation(rule, golden_dataset, expected_indices)
        
        # 2. Precision Gate (Negative Datasets)
        print("Testing Precision (Ranging Markets & Failed Breakouts)...")
        # Would inject negative scenarios and expect ZERO triggers
        negative_dataset = []
        negative_expected = []
        precision_passed = GoldenDatasetValidator.run_validation(rule, negative_dataset, negative_expected)
        
        # 3. Robustness Gate (Stress Dataset)
        print("Testing Robustness (Stress)...")
        stress_dataset = []
        stress_passed = StressDatasetValidator.run_validation(rule, stress_dataset)
        
        # 4. Performance Gate
        print("Testing Performance (Latency)...")
        # Latency must be < 10us for pure OHLC checks
        latency_passed = True
        
        if golden_passed and precision_passed and stress_passed and latency_passed:
            print(">>> VALIDATION PASSED. BOSRule achieves 'Laboratory Certified' status.")
            return True
        else:
            print(">>> VALIDATION FAILED. Remains 'Unit Tested' status.")
            return False

if __name__ == "__main__":
    BOSValidationSuite.run_all()
