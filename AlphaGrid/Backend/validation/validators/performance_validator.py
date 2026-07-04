import os
import json
import time
import numpy as np
import pandas as pd
from typing import Dict, Any
from Backend.validation.validators.abstract_validator import AbstractValidator
from Backend.validation.dtos import ValidationContextDTO, ValidatorResultDTO

from Backend.reference.legacy.features.macd import MACDLegacyGenerator
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
        
        benchmark_data = {
            "latency_ms_before": leg_time,
            "latency_ms_after": new_time,
            "improvement_ratio": leg_time / max(new_time, 1e-6),
            "iterations": 100,
            "dataset_size": size
        }
        with open(os.path.join(ev_dir, "benchmark.json"), "w") as f:
            json.dump(benchmark_data, f, indent=4)
            
        import platform
        import subprocess
        try:
            import psutil
            cpu_percent = psutil.cpu_percent()
            ram_percent = psutil.virtual_memory().percent
        except ImportError:
            cpu_percent = -1
            ram_percent = -1
            
        try:
            git_sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode('utf-8').strip()
        except Exception:
            git_sha = "unknown"
            
        env_data = {
            "cpu_model": platform.processor(),
            "cpu_cores": os.cpu_count(),
            "os_build": platform.version(),
            "cpu_percent": cpu_percent,
            "ram_percent": ram_percent,
            "python_version": platform.python_version(),
            "numpy_version": np.__version__,
            "pandas_version": pd.__version__,
            "git_commit_sha": git_sha,
            "benchmark_seed": 99
        }
        with open(os.path.join(ev_dir, "environment.json"), "w") as f:
            json.dump(env_data, f, indent=4)
            
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
