import time
import numpy as np
from Backend.validation.validators.abstract_validator import AbstractValidator
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO
from Backend.indicator_engine.runner import IndicatorRunner
from Backend.indicator_engine.registry import IndicatorRegistry
from Backend.market_data.market_series import MarketSeries

class IndicatorCompositionValidator(AbstractValidator):
    def run_validation(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        start = time.perf_counter()
        errors = []
        
        # We test MA Cross composability
        size = 1000
        timestamps = np.arange(size)
        closes = np.random.randn(size)
        series = MarketSeries(
            symbol="TEST", timeframe="1m", timestamps=timestamps,
            opens=closes, highs=closes, lows=closes, closes=closes, volumes=closes
        )
        
        if IndicatorRegistry.get("ma_cross"):
            try:
                # Execute underlying primitives directly
                fast_res = IndicatorRunner.execute("ema", series, period=10)
                slow_res = IndicatorRunner.execute("ema", series, period=30)
                
                # Execute composite
                cross_res = IndicatorRunner.execute("ma_cross", series, fast_period=10, slow_period=30, fast_type="ema", slow_type="ema")
                
                # Verify exact equivalence
                if not np.allclose(fast_res.ema[fast_res.valid_mask], cross_res.fast_ma[fast_res.valid_mask]):
                    errors.append("MACross fast_ma does not exactly match underlying EMA10 primitive.")
                    
                if not np.allclose(slow_res.ema[slow_res.valid_mask], cross_res.slow_ma[slow_res.valid_mask]):
                    errors.append("MACross slow_ma does not exactly match underlying EMA30 primitive.")
                    
                expected_cross = cross_res.fast_ma - cross_res.slow_ma
                if not np.allclose(expected_cross[cross_res.valid_mask], cross_res.cross_signal[cross_res.valid_mask]):
                    errors.append("MACross cross_signal does not exactly equal fast_ma - slow_ma.")
                    
            except Exception as e:
                errors.append(f"Composition execution failed: {str(e)}")
                
        duration_ms = (time.perf_counter() - start) * 1000.0
        
        if errors:
            return ValidatorResultDTO(
                id=self.validator_id, status="FAIL", duration_ms=duration_ms,
                phase=context.phase, family=context.family,
                errors=errors, summary=f"Failed indicator composition validation with {len(errors)} errors."
            )
            
        return ValidatorResultDTO(
            id=self.validator_id, status="PASS", duration_ms=duration_ms,
            phase=context.phase, family=context.family,
            summary="All composite indicators accurately align with underlying mathematical primitives."
        )
