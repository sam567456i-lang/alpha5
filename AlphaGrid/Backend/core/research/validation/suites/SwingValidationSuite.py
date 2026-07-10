from Backend.core.methodologies.rules.library.SwingValidationRule import SwingValidationRule
from Backend.core.methodologies.rules.library.SwingValidationRulePolicy import SwingValidationPolicy
from Backend.core.research.validation.rule_validators import GoldenDatasetValidator, StressDatasetValidator

class SwingValidationSuite:
    """The automated laboratory validation pipeline for the SwingValidationRule."""
    
    @staticmethod
    def run_all():
        print("Starting Validation Suite for SwingValidationRule...")
        policy = SwingValidationPolicy()
        rule = SwingValidationRule(policy=policy, version="1.0.0")
        
        # 1. Correctness Gate (Golden Datasets)
        print("Testing Correctness (Perfect >1.5 ATR Swings)...")
        golden_dataset = [] 
        expected_indices = []
        golden_passed = GoldenDatasetValidator.run_validation(rule, golden_dataset, expected_indices)
        
        # 2. Precision Gate (Negative Datasets)
        print("Testing Precision (Micro-swings < 1.0 ATR)...")
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
            print(">>> VALIDATION PASSED. SwingValidationRule achieves 'Laboratory Certified' status.")
            return True
        else:
            print(">>> VALIDATION FAILED. Remains 'Unit Tested' status.")
            return False

if __name__ == "__main__":
    SwingValidationSuite.run_all()
