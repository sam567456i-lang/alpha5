import os
import time
import numpy as np
import pandas as pd
from Backend.validation.validators.abstract_validator import AbstractValidator
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO
from Backend.math.public.ema import calculate_ema
from Backend.math.public.sma import calculate_sma
from Backend.math.public.wma import calculate_wma
from Backend.math.public.rolling_sum import calculate_rolling_sum
from Backend.math.public.rolling_max import calculate_rolling_max
from Backend.math.public.rolling_min import calculate_rolling_min
from Backend.math.public.diff import calculate_diff
from Backend.math.public.shift import calculate_shift
from Backend.math.public.variance import calculate_variance
from Backend.math.public.stddev import calculate_stddev
from Backend.math.public.covariance import calculate_covariance
from Backend.math.public.correlation import calculate_correlation

class NumericalPrecisionValidator(AbstractValidator):
    def run_validation(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        start = time.perf_counter()
        golden_path = os.path.join(context.workspace, "Datasets", "golden", "reference.parquet")
        
        if not os.path.exists(golden_path):
            return ValidatorResultDTO(
                id=self.validator_id, status="SKIPPED", reason="Missing reference.parquet",
                phase=context.phase, family=context.family
            )
            
        try:
            df = pd.read_parquet(golden_path)
        except Exception as e:
            return ValidatorResultDTO(
                id=self.validator_id, status="ERROR", reason=f"Failed to read parquet: {str(e)}",
                phase=context.phase, family=context.family
            )
            
        prices = df['close'].values.astype(np.float64)
        volume = df['volume'].values.astype(np.float64)
        timestamps = np.arange(len(prices))
        period = 14
        
        errors = []
        metrics = {}
        
        tolerances = {
            "ema": 1e-12,
            "sma": 1e-12,
            "var": 1e-10
        }
        
        def calculate_metrics(name, res, expected, tol):
            valid = res.valid_mask
            expected_valid = expected[valid]
            actual_valid = res.values[valid]
            
            if len(expected_valid) == 0:
                return
                
            abs_diff = np.abs(actual_valid - expected_valid)
            # Avoid division by zero in relative error
            with np.errstate(divide='ignore', invalid='ignore'):
                rel_diff = np.abs(abs_diff / expected_valid)
                rel_diff[np.isnan(rel_diff) | np.isinf(rel_diff)] = 0.0
                
            max_abs = float(np.max(abs_diff))
            mean_abs = float(np.mean(abs_diff))
            max_rel = float(np.max(rel_diff))
            mean_rel = float(np.mean(rel_diff))
            
            metrics[name] = {
                "max_absolute_error": max_abs,
                "mean_absolute_error": mean_abs,
                "max_relative_error": max_rel,
                "mean_relative_error": mean_rel,
                "tolerance_applied": tol
            }
            
            if max_abs > tol:
                errors.append(f"{name} precision failed: Max abs err {max_abs} > {tol}")
                
        # 1. Check EMA
        ema_res = calculate_ema(prices, timestamps, period)
        calculate_metrics("EMA", ema_res, df['ema_14'].values, tolerances["ema"])
                
        # 2. Check SMA
        sma_res = calculate_sma(prices, timestamps, period)
        calculate_metrics("SMA", sma_res, df['sma_14'].values, tolerances["sma"])
                
        # 3. Check Variance
        var_res = calculate_variance(prices, timestamps, period, ddof=1)
        calculate_metrics("Variance", var_res, df['var_14'].values, tolerances["var"])
                
        # 4. Check all new Wave 0 Primitives
        wma_res = calculate_wma(prices, timestamps, period)
        calculate_metrics("WMA", wma_res, df['wma_14'].values, tolerances["sma"])
        
        std_res = calculate_stddev(prices, timestamps, period, ddof=1)
        calculate_metrics("StdDev", std_res, df['std_14'].values, tolerances["var"])
        
        roll_max_res = calculate_rolling_max(prices, timestamps, period)
        calculate_metrics("Rolling_Max", roll_max_res, df['roll_max_14'].values, tolerances["sma"])
        
        roll_min_res = calculate_rolling_min(prices, timestamps, period)
        calculate_metrics("Rolling_Min", roll_min_res, df['roll_min_14'].values, tolerances["sma"])
        
        diff_res = calculate_diff(prices, timestamps, period)
        calculate_metrics("Diff", diff_res, df['diff_14'].values, tolerances["sma"])
        
        shift_res = calculate_shift(prices, timestamps, period)
        calculate_metrics("Shift", shift_res, df['shift_14'].values, tolerances["sma"])
        
        cov_res = calculate_covariance(prices, volume, timestamps, period)
        calculate_metrics("Covariance", cov_res, df['cov_14'].values, tolerances["var"])
        
        corr_res = calculate_correlation(prices, volume, timestamps, period)
        calculate_metrics("Correlation", corr_res, df['corr_14'].values, tolerances["var"])
                
        duration_ms = (time.perf_counter() - start) * 1000.0
        
        # Calculate aggregate
        global_max_abs = max([m["max_absolute_error"] for m in metrics.values()]) if metrics else 0.0
        global_mean_abs = sum([m["mean_absolute_error"] for m in metrics.values()]) / len(metrics) if metrics else 0.0
        
        if errors:
            return ValidatorResultDTO(
                id=self.validator_id, status="FAIL", duration_ms=duration_ms,
                phase=context.phase, family=context.family,
                errors=errors, metrics=metrics,
                max_error=global_max_abs, mean_error=global_mean_abs,
                summary=f"Failed {len(errors)} precision tolerance bounds."
            )
            
        return ValidatorResultDTO(
            id=self.validator_id, status="PASS", duration_ms=duration_ms,
            phase=context.phase, family=context.family,
            metrics=metrics,
            max_error=global_max_abs, mean_error=global_mean_abs,
            summary="All numerical primitives match golden datasets within strict tolerances."
        )
