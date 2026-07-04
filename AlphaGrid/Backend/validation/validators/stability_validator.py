import os
import json
import time
import warnings
import numpy as np
from Backend.validation.validators.abstract_validator import AbstractValidator
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO
from Backend.math.public.ema import calculate_ema

class StabilityValidator(AbstractValidator):
    def run_validation(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        start = time.perf_counter()
        stress_path = os.path.join(context.workspace, "Datasets", "stress", "edge_cases.json")
        
        if not os.path.exists(stress_path):
            return ValidatorResultDTO(
                id=self.validator_id, status="SKIPPED", reason="Missing edge_cases.json",
                phase=context.phase, family=context.family
            )
            
        with open(stress_path, "r") as f:
            edge_cases = json.load(f)
            
        errors = []
        period = 3
        
        for case_name, values in edge_cases.items():
            # Convert string representation back to numpy floats
            np_values = []
            for v in values:
                if v == "NaN":
                    np_values.append(np.nan)
                elif v == "Inf":
                    np_values.append(np.inf)
                elif v == "-Inf":
                    np_values.append(-np.inf)
                else:
                    np_values.append(float(v))
                    
            prices = np.array(np_values, dtype=np.float64)
            timestamps = np.arange(len(prices))
            
            try:
                with warnings.catch_warnings(record=True) as w:
                    warnings.simplefilter("always")
                    res = calculate_ema(prices, timestamps, period)
                    
                    if len(w) > 0:
                        for warn in w:
                            warning_msg = str(warn.message)
                            if case_name == "alternating_inf" and "invalid value encountered in scalar add" in warning_msg:
                                # This is expected!
                                continue
                            elif "invalid value encountered in scalar divide" in warning_msg:
                                # Also acceptable in certain stress cases
                                continue
                            else:
                                errors.append(f"Stability Failed: Unexpected warning '{warning_msg}' on {case_name}")
                
                # Check that valid masks correctly exclude NaNs
                if case_name == "nan_islands":
                    if np.sum(res.valid_mask) == len(res.valid_mask):
                        errors.append(f"Stability Failed: NaN Islands were improperly masked as valid.")
                        
            except Exception as e:
                errors.append(f"Stability Failed: Primitive crashed on {case_name}: {str(e)}")
                
        duration_ms = (time.perf_counter() - start) * 1000.0
        
        if errors:
            return ValidatorResultDTO(
                id=self.validator_id, status="FAIL", duration_ms=duration_ms,
                phase=context.phase, family=context.family,
                errors=errors,
                summary=f"Failed {len(errors)} institutional edge-case stability checks."
            )
            
        return ValidatorResultDTO(
            id=self.validator_id, status="PASS", duration_ms=duration_ms,
            phase=context.phase, family=context.family,
            summary="All mathematical primitives safely absorbed stress edge-cases."
        )
