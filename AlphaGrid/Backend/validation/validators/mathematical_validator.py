import os
import json
import time
import numpy as np
from Backend.validation.validators.abstract_validator import AbstractValidator
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO
from Backend.math.public.ema import calculate_ema
from Backend.math.public.sma import calculate_sma
from Backend.math.public.rolling_sum import calculate_rolling_sum
from Backend.math.public.variance import calculate_variance
from Backend.math.public.correlation import calculate_correlation

class MathematicalValidator(AbstractValidator):
    def run_validation(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        start = time.perf_counter()
        identities_path = os.path.join(context.workspace, "Datasets", "synthetic", "math_identities.json")
        
        if not os.path.exists(identities_path):
            return ValidatorResultDTO(
                id=self.validator_id, status="SKIPPED", reason="Missing Datasets/synthetic/math_identities.json",
                phase=context.phase, family=context.family
            )
            
        with open(identities_path, "r") as f:
            data = json.load(f)
            
        prices = np.array(data["prices"], dtype=np.float64)
        timestamps = np.array(data["timestamps"], dtype=np.int64)
        period = 14
        
        errors = []
        max_err = 0.0
        
        def assert_identity(name: str, actual: np.ndarray, expected: np.ndarray, mask: np.ndarray, tol: float = 1e-12):
            nonlocal max_err
            diff = np.abs(actual[mask] - expected[mask])
            if len(diff) > 0:
                local_max = np.max(diff)
                max_err = max(max_err, local_max)
                if local_max > tol:
                    errors.append(f"Identity Failed: {name} (Max error: {local_max})")
        
        # 1. Rolling Mean == Rolling Sum / Period
        sma_res = calculate_sma(prices, timestamps, period)
        sum_res = calculate_rolling_sum(prices, timestamps, period)
        assert_identity("Rolling Mean == Rolling Sum / Period", sma_res.values, sum_res.values / period, sma_res.valid_mask)
                
        # 2. Linearity of EMA: EMA(x + c) == EMA(x) + c
        c = 100.0
        ema_res_base = calculate_ema(prices, timestamps, period)
        ema_res_shift = calculate_ema(prices + c, timestamps, period)
        assert_identity("EMA(x + c) == EMA(x) + c", ema_res_shift.values, ema_res_base.values + c, ema_res_base.valid_mask)
        
        # 3. Variance(Constant) == 0
        const_arr = np.full(len(prices), 42.0, dtype=np.float64)
        var_res = calculate_variance(const_arr, timestamps, period, ddof=1)
        expected_zeros = np.zeros(len(prices))
        assert_identity("Variance(c) == 0", var_res.values, expected_zeros, var_res.valid_mask)
        
        # 4. Correlation(x, x) == 1
        # Add some noise to x so variance isn't exactly 0 (which would make corr undefined)
        x_noise = prices + np.random.randn(len(prices)) * 0.001
        corr_res = calculate_correlation(x_noise, x_noise, timestamps, period)
        expected_ones = np.ones(len(prices))
        assert_identity("Correlation(x, x) == 1", corr_res.values, expected_ones, corr_res.valid_mask)
        
        # 5. SMA(Constant) == Constant
        sma_const = calculate_sma(const_arr, timestamps, period)
        assert_identity("SMA(Constant) == Constant", sma_const.values, const_arr, sma_const.valid_mask)
                
        # 6. Triple-Reference Equivalence Proof (Math Core == Indicator Engine == Feature Generator)
        from Backend.market_data.market_series import MarketSeries
        from Backend.indicator_engine.trend.moving_averages import SMAEngine
        from Backend.features.sma_generator import SMAFeatureGenerator
        import pandas as pd
        
        # Construct MarketSeries
        df = pd.DataFrame({"close": prices}, index=pd.to_datetime(timestamps, unit="ns"))
        series = MarketSeries(
            symbol="TEST",
            timeframe="1d",
            timestamps=timestamps,
            opens=prices,
            highs=prices,
            lows=prices,
            closes=prices,
            volumes=prices
        )
        
        # Engine
        engine = SMAEngine(period=period)
        engine_res = engine.generate(series)
        
        # Feature
        feature = SMAFeatureGenerator(period=period)
        feature_res = feature.generate(df, trace_id="123", correlation_id="456")
        
        # Assert Math Core == Engine == Feature
        assert_identity("Triple-Reference (Core == Engine)", sma_res.values, engine_res.sma, sma_res.valid_mask)
        
        last_val = float(sma_res.values[-1])
        feat_val = float(feature_res.values['sma'])
        if abs(last_val - feat_val) > 1e-9:
            errors.append(f"Triple-Reference (Core == Feature) failed: {feat_val} != {last_val}")
        
        duration_ms = (time.perf_counter() - start) * 1000.0
        
        if errors:
            return ValidatorResultDTO(
                id=self.validator_id, status="FAIL", duration_ms=duration_ms,
                phase=context.phase, family=context.family,
                errors=errors, max_error=float(max_err),
                summary=f"Failed {len(errors)} mathematical identities."
            )
            
        return ValidatorResultDTO(
            id=self.validator_id, status="PASS", duration_ms=duration_ms,
            phase=context.phase, family=context.family,
            max_error=float(max_err),
            summary="All mathematical identity proofs passed."
        )
