from typing import List, Dict, Any
import random
from Backend.core.methodologies.rules.library.liquidity_sweep import LiquiditySweepRule
from Backend.core.methodologies.rules.sdk.rule_context import RuleContext
from Backend.core.data_foundation.contracts.schemas import OHLCSchema
from datetime import datetime

class GoldenDatasetValidator:
    """Runs a rule against a mathematically perfect dataset to prove Correctness."""
    
    @staticmethod
    def run_validation(rule, golden_dataset: List[OHLCSchema], expected_trigger_indices: List[int]) -> bool:
        pass_count = 0
        false_positives = 0
        
        for i, bar in enumerate(golden_dataset):
            context = RuleContext(
                historical_bars=golden_dataset[:i],
                current_bar=bar,
                market_regime="PERFECT_RANGE",
                active_dataset_id="GOLDEN_001",
                parameters={"tolerance": 0.05}
            )
            result = rule.evaluate(context)
            
            if result.did_trigger:
                if i in expected_trigger_indices:
                    pass_count += 1
                else:
                    false_positives += 1
                    
        expected_total = len(expected_trigger_indices)
        print(f"[{rule.rule_id}] Golden Validation: {pass_count}/{expected_total} detected. False Positives: {false_positives}")
        
        # 100% Correctness required
        return pass_count == expected_total and false_positives == 0

class StressDatasetValidator:
    """Runs a rule against corrupted data to prove Robustness."""
    
    @staticmethod
    def run_validation(rule, stress_dataset: List[OHLCSchema]) -> bool:
        # We expect the rule NOT to crash when facing corrupt data (e.g. missing volume)
        try:
            for i, bar in enumerate(stress_dataset):
                context = RuleContext(
                    historical_bars=stress_dataset[:i],
                    current_bar=bar,
                    market_regime="STRESS",
                    active_dataset_id="STRESS_001",
                    parameters={}
                )
                rule.evaluate(context)
            print(f"[{rule.rule_id}] Stress Validation: PASSED (No crashes).")
            return True
        except Exception as e:
            print(f"[{rule.rule_id}] Stress Validation: FAILED (Crashed with {e}).")
            return False
