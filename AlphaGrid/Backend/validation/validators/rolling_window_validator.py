import time
import numpy as np
from Backend.validation.validators.abstract_validator import AbstractValidator
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO
from Backend.indicator_engine.runner import IndicatorRunner
from Backend.indicator_engine.registry import IndicatorRegistry
from Backend.market_data.market_series import MarketSeries

class RollingWindowValidator(AbstractValidator):
    def run_validation(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        start = time.perf_counter()
        errors = []
        
        # Test indicators that use rolling accumulation like ATR and Bollinger
        size = 100
        timestamps = np.arange(size)
        closes = np.arange(1.0, size + 1.0) # Linearly increasing prices
        series = MarketSeries(
            symbol="TEST", timeframe="1m", timestamps=timestamps,
            opens=closes, highs=closes + 1, lows=closes - 1, closes=closes, volumes=closes
        )
        
        # Validate Bollinger Bands (SMA-based rolling window)
        if IndicatorRegistry.get("bollinger"):
            try:
                bb_res = IndicatorRunner.execute("bollinger", series, period=20, std_dev=2.0)
                
                # Check first valid index
                first_valid_idx = np.where(bb_res.valid_mask)[0][0]
                if first_valid_idx != 19:  # period - 1
                    errors.append(f"Bollinger Bands first valid index is {first_valid_idx}, expected 19.")
                
                # Check no off-by-one by ensuring the SMA matches manual calculation
                expected_sma_idx20 = np.mean(closes[1:21])
                if not np.isclose(bb_res.middle[20], expected_sma_idx20):
                    errors.append(f"Bollinger Bands middle line at index 20 is {bb_res.middle[20]}, expected {expected_sma_idx20}.")
                    
            except Exception as e:
                errors.append(f"Bollinger Bands execution failed: {str(e)}")
                
        # Validate ATR (RMA-based rolling accumulation)
        if IndicatorRegistry.get("atr"):
            try:
                atr_res = IndicatorRunner.execute("atr", series, period=14, smoothing="rma")
                
                # Check first valid index
                first_valid_idx = np.where(atr_res.valid_mask)[0][0]
                if first_valid_idx != 13:  # period - 1 (since TR is seeded at index 0)
                    errors.append(f"ATR first valid index is {first_valid_idx}, expected 13.")
                    
                # The TR is a constant 2.0 (High - Low). So ATR should stabilize at 2.0.
                if not np.allclose(atr_res.atr[first_valid_idx:], 2.0):
                    errors.append("ATR did not accumulate constant TR correctly.")
                    
            except Exception as e:
                errors.append(f"ATR execution failed: {str(e)}")
                
        duration_ms = (time.perf_counter() - start) * 1000.0
        
        if errors:
            return ValidatorResultDTO(
                id=self.validator_id, status="FAIL", duration_ms=duration_ms,
                phase=context.phase, family=context.family,
                errors=errors, summary=f"Failed rolling window validation with {len(errors)} errors."
            )
            
        return ValidatorResultDTO(
            id=self.validator_id, status="PASS", duration_ms=duration_ms,
            phase=context.phase, family=context.family,
            summary="All rolling window indicators passed boundary and accumulation validation."
        )
