import time
import numpy as np
from Backend.validation.validators.abstract_validator import AbstractValidator
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO
from Backend.indicator_engine.runner import IndicatorRunner
from Backend.market_data.market_series import MarketSeries
from Backend.indicator_engine.registry import IndicatorRegistry

class IndicatorWarmupValidator(AbstractValidator):
    def run_validation(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        start = time.perf_counter()
        errors = []
        
        size = 100
        timestamps = np.arange(size)
        closes = np.random.randn(size)
        series = MarketSeries(
            symbol="TEST", timeframe="1m", timestamps=timestamps,
            opens=closes, highs=closes, lows=closes, closes=closes, volumes=closes
        )
        
        for name, registration in IndicatorRegistry.get_all().items():
            try:
                res = IndicatorRunner.execute(name, series)
                if not hasattr(res, "warmup_period") or res.warmup_period is None:
                    errors.append(f"Indicator '{name}' is missing a warmup period in its result.")
            except Exception as e:
                errors.append(f"Indicator warmup failed for '{name}': {str(e)}")
        
        duration_ms = (time.perf_counter() - start) * 1000.0
        
        if errors:
            return ValidatorResultDTO(
                id=self.validator_id, status="FAIL", duration_ms=duration_ms,
                phase=context.phase, family=context.family,
                errors=errors, summary=f"Failed warmup validation with {len(errors)} errors."
            )
            
        return ValidatorResultDTO(
            id=self.validator_id, status="PASS", duration_ms=duration_ms,
            phase=context.phase, family=context.family,
            summary="All indicators correctly expose warmup behavior."
        )
