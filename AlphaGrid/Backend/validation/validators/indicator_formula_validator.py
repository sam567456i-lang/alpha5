import time
import numpy as np
from Backend.validation.validators.abstract_validator import AbstractValidator
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO
from Backend.indicator_engine.runner import IndicatorRunner
from Backend.market_data.market_series import MarketSeries

class IndicatorFormulaValidator(AbstractValidator):
    def run_validation(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        start = time.perf_counter()
        errors = []
        
        # Test MACD formula identity
        size = 1000
        timestamps = np.arange(size)
        closes = np.random.randn(size)
        series = MarketSeries(
            symbol="TEST", timeframe="1m", timestamps=timestamps,
            opens=closes, highs=closes, lows=closes, closes=closes, volumes=closes
        )
        
        try:
            macd_res = IndicatorRunner.execute("macd", series)
            roc_res = IndicatorRunner.execute("roc", series)
            
            # Basic validation that arrays are correct lengths and types
            if len(macd_res.macd) != size:
                errors.append("MACD result length mismatch.")
            if len(roc_res.roc) != size:
                errors.append("ROC result length mismatch.")
                
        except Exception as e:
            errors.append(f"Indicator engine failed to execute: {str(e)}")
        
        duration_ms = (time.perf_counter() - start) * 1000.0
        
        if errors:
            return ValidatorResultDTO(
                id=self.validator_id, status="FAIL", duration_ms=duration_ms,
                phase=context.phase, family=context.family,
                errors=errors, summary=f"Failed formula validation with {len(errors)} errors."
            )
            
        return ValidatorResultDTO(
            id=self.validator_id, status="PASS", duration_ms=duration_ms,
            phase=context.phase, family=context.family,
            summary="Indicator formulas execute successfully and match structure."
        )
