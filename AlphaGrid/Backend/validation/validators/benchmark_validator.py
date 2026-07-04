import time
import numpy as np
from Backend.validation.validators.abstract_validator import AbstractValidator
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO
from Backend.math.public.ema import calculate_ema

class BenchmarkValidator(AbstractValidator):
    def run_validation(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        start = time.perf_counter()
        
        sizes = [1000, 10000, 100000]
        period = 14
        passes = 5
        
        errors = []
        metrics = {}
        prev_avg_time = None
        
        for size in sizes:
            values = np.random.randn(size)
            timestamps = np.arange(size)
            
            # Cold cache pass
            _ = calculate_ema(values, timestamps, period)
            
            # Warm cache passes for EMA
            pass_times = []
            roc_pass_times = []
            
            from Backend.math.public.roc import calculate_roc
            
            for _ in range(passes):
                t0 = time.perf_counter()
                _ = calculate_ema(values, timestamps, period)
                t1 = time.perf_counter()
                pass_times.append((t1 - t0) * 1000.0)
                
                t2 = time.perf_counter()
                _ = calculate_roc(values, timestamps, period)
                t3 = time.perf_counter()
                roc_pass_times.append((t3 - t2) * 1000.0)
                
            avg_ms = float(np.mean(pass_times))
            median_ms = float(np.median(pass_times))
            std_ms = float(np.std(pass_times))
            p95_ms = float(np.percentile(pass_times, 95))
            
            roc_avg_ms = float(np.mean(roc_pass_times))
            
            metrics[f"ema_{size}"] = {
                "average_ms": avg_ms,
                "median_ms": median_ms,
                "std_ms": std_ms,
                "p95_ms": p95_ms
            }
            
            metrics[f"roc_{size}"] = {
                "average_ms": roc_avg_ms
            }
            
            if prev_avg_time is not None:
                scaling = avg_ms / prev_avg_time
                if scaling > 25.0:
                    errors.append(f"O(N) empirical scaling failed: Factor {scaling:.1f}x from {size//10} to {size}.")
                    
            prev_avg_time = avg_ms
            
        total_duration_ms = (time.perf_counter() - start) * 1000.0
        
        if errors:
            return ValidatorResultDTO(
                id=self.validator_id, status="FAIL", duration_ms=total_duration_ms,
                phase=context.phase, family=context.family,
                errors=errors, metrics=metrics,
                summary=f"Failed {len(errors)} benchmark complexity bounds."
            )
            
        return ValidatorResultDTO(
            id=self.validator_id, status="PASS", duration_ms=total_duration_ms,
            phase=context.phase, family=context.family, metrics=metrics,
            summary="Observed runtime remained approximately linear and did not indicate quadratic growth."
        )
