import os
import json
import time
import numpy as np
import pandas as pd
from typing import Dict, Any
from Backend.validation.validators.abstract_validator import AbstractValidator
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO

from Backend.features.legacy.macd_legacy import MACDLegacyGenerator
from Backend.features.macd_generator import MACDFeatureGenerator

class PerformanceValidator(AbstractValidator):
    def run_validation(self, context: ValidationContextDTO) -> ValidatorResultDTO:
        start = time.perf_counter()
        
        # We use a purely synthetic large dataset for pure benchmarking
        np.random.seed(99)
        size = 50000
        df = pd.DataFrame({
            "close": np.random.randn(size) * 10 + 100,
            "volume": np.random.randint(100, 1000, size)
        })
        df.attrs['symbol'] = 'PERF'
        df.attrs['timeframe'] = '1m'
        
        legacy_gen = MACDLegacyGenerator()
        new_gen = MACDFeatureGenerator()
        
        # Profile Legacy
        leg_start = time.perf_counter()
        for _ in range(100):
            _ = legacy_gen.generate(df, "trace", "corr")
        leg_time = (time.perf_counter() - leg_start) * 10.0 # scale to ms per call
        
        # Profile New
        # Warmup Numba compiler
        _ = new_gen.generate(df.iloc[:100], "trace", "corr")
        
        new_start = time.perf_counter()
        for _ in range(100):
            _ = new_gen.generate(df, "trace", "corr")
        new_time = (time.perf_counter() - new_start) * 10.0 # scale to ms per call
        
        ev_dir = os.path.join(context.workspace, "Docs", "Evidence", "2026", context.phase)
        os.makedirs(ev_dir, exist_ok=True)
        
        with open(os.path.join(ev_dir, "performance_before.json"), "w") as f:
            json.dump({"latency_ms": leg_time}, f)
            
        with open(os.path.join(ev_dir, "performance_after.json"), "w") as f:
            json.dump({"latency_ms": new_time, "improvement_ratio": leg_time / max(new_time, 1e-6)}, f)
            
        duration_ms = (time.perf_counter() - start) * 1000.0
        
        if new_time > leg_time * 1.5:
            return ValidatorResultDTO(
                id=self.validator_id, status="FAIL", duration_ms=duration_ms,
                phase=context.phase, family=context.family,
                errors=[f"Performance regression detected! Old: {leg_time:.2f}ms, New: {new_time:.2f}ms"],
                summary="New implementation is significantly slower."
            )
            
        return ValidatorResultDTO(
            id=self.validator_id, status="PASS", duration_ms=duration_ms,
            phase=context.phase, family=context.family,
            summary=f"Performance check passed. Old: {leg_time:.2f}ms, New: {new_time:.2f}ms."
        )
