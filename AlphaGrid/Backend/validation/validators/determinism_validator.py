import time
import hashlib
import numpy as np
from Backend.validation.validators.abstract_validator import AbstractValidator
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO
from Backend.math import public

class DeterminismValidator(AbstractValidator):
    def run_validation(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        start = time.perf_counter()
        
        # Test vector
        np.random.seed(42)
        size = 1000
        prices = np.random.randn(size) * 10 + 100
        volume = np.random.randn(size) * 100 + 1000
        timestamps = np.arange(size)
        period = 14
        
        def compute_hash(arr):
            safe_arr = np.nan_to_num(arr, nan=-999.0)
            return hashlib.sha256(safe_arr.tobytes()).hexdigest()
            
        errors = []
        
        primitives_1_arg = [
            ("EMA", public.calculate_ema),
            ("SMA", public.calculate_sma),
            ("WMA", public.calculate_wma),
            ("ROLL_SUM", public.calculate_rolling_sum),
            ("ROLL_MAX", public.calculate_rolling_max),
            ("ROLL_MIN", public.calculate_rolling_min),
            ("DIFF", public.calculate_diff),
            ("SHIFT", public.calculate_shift),
            ("VARIANCE", public.calculate_variance),
            ("STDDEV", public.calculate_stddev)
        ]
        
        primitives_2_arg = [
            ("COVARIANCE", public.calculate_covariance),
            ("CORRELATION", public.calculate_correlation)
        ]
        
        # 1-Arg Primitives
        for name, func in primitives_1_arg:
            res1 = func(prices, timestamps, period)
            hash1 = compute_hash(res1.values)
            
            res2 = func(prices, timestamps, period)
            hash2 = compute_hash(res2.values)
            
            if hash1 != hash2:
                errors.append(f"Determinism Failed for {name}: Pass 1 hash ({hash1}) != Pass 2 hash ({hash2})")
                
        # 2-Arg Primitives
        for name, func in primitives_2_arg:
            res1 = func(prices, volume, timestamps, period)
            hash1 = compute_hash(res1.values)
            
            res2 = func(prices, volume, timestamps, period)
            hash2 = compute_hash(res2.values)
            
            if hash1 != hash2:
                errors.append(f"Determinism Failed for {name}: Pass 1 hash ({hash1}) != Pass 2 hash ({hash2})")
                
        # 0-Arg Primitives (Clip)
        res1 = public.calculate_clip(prices, timestamps, 90.0, 110.0)
        hash1 = compute_hash(res1.values)
        res2 = public.calculate_clip(prices, timestamps, 90.0, 110.0)
        hash2 = compute_hash(res2.values)
        if hash1 != hash2:
            errors.append(f"Determinism Failed for CLIP: Pass 1 hash ({hash1}) != Pass 2 hash ({hash2})")
            
        duration_ms = (time.perf_counter() - start) * 1000.0
        
        if errors:
            return ValidatorResultDTO(
                id=self.validator_id, status="FAIL", duration_ms=duration_ms,
                phase=context.phase, family=context.family,
                errors=errors,
                summary="Failed determinism verification: Mathematical primitive output varies across identical inputs."
            )
            
        return ValidatorResultDTO(
            id=self.validator_id, status="PASS", duration_ms=duration_ms,
            phase=context.phase, family=context.family,
            summary="All mathematical primitives proven to be strictly deterministic with no hidden state."
        )
