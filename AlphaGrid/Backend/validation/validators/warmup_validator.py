import time
import numpy as np
from Backend.validation.validators.abstract_validator import AbstractValidator
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO
from Backend.math.public.ema import calculate_ema

class WarmupValidator(AbstractValidator):
    def run_validation(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        start = time.perf_counter()
        
        period = 14
        prices = np.ones(100)
        timestamps = np.arange(100)
        
        errors = []
        
        ema_res = calculate_ema(prices, timestamps, period)
        
        # 1. Output Array Length
        if len(ema_res.values) != len(prices):
            errors.append("Output array length does not match input array length.")
            
        # 2. Strict Timestamp Alignment
        if not np.array_equal(ema_res.timestamps, timestamps):
            errors.append("Output timestamps do not identically match input timestamps.")
            
        # 3. Warmup Region NaN integrity
        warmup_region = ema_res.values[:ema_res.warmup_period]
        if not np.isnan(warmup_region).all():
            errors.append(f"First {ema_res.warmup_period} elements must be strictly NaN.")
            
        # 4. Valid Mask Boundary
        if ema_res.valid_mask[:ema_res.warmup_period].any():
            errors.append("Valid mask must be strictly False during warmup.")
            
        # 5. First Valid Element
        if not ema_res.valid_mask[ema_res.warmup_period]:
            errors.append("First element after warmup must be valid.")
            
        # 6. Minimum History Safety
        short_prices = np.ones(5)
        short_timestamps = np.arange(5)
        short_res = calculate_ema(short_prices, short_timestamps, period)
        if short_res.valid_mask.any():
            errors.append("Arrays shorter than lookback must return all-False valid_mask.")
            
        duration_ms = (time.perf_counter() - start) * 1000.0
        
        if errors:
            return ValidatorResultDTO(
                id=self.validator_id, status="FAIL", duration_ms=duration_ms,
                phase=context.phase, family=context.family,
                errors=errors,
                summary=f"Failed {len(errors)} warmup constraints."
            )
            
        return ValidatorResultDTO(
            id=self.validator_id, status="PASS", duration_ms=duration_ms,
            phase=context.phase, family=context.family,
            summary="All mathematical primitives strictly adhere to warmup boundaries."
        )
