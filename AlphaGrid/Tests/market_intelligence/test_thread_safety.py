import pytest
import pandas as pd
from datetime import datetime, timezone
import concurrent.futures

from Backend.market_intelligence.normalization_engine import NormalizationEngine
from Backend.market_intelligence.mtf_alignment_engine import MTFAlignmentEngine

class TestThreadSafety:
    def setup_method(self):
        # Engines must be stateless and thread-safe
        self.norm_engine = NormalizationEngine()
        self.mtf_engine = MTFAlignmentEngine()
        
        # Base datasets
        idx_lower = pd.date_range("2026-07-01 09:15:00", periods=100, freq="1min", tz="UTC")
        self.raw_lower = pd.DataFrame({
            "open": range(100, 200),
            "high": range(101, 201),
            "low": range(99, 199),
            "close": range(100, 200),
            "volume": [1000] * 100
        }, index=idx_lower)
        
        idx_higher = pd.date_range("2026-07-01 09:15:00", periods=5, freq="15min", tz="UTC")
        self.raw_higher = pd.DataFrame({
            "open": [100, 115, 130, 145, 160],
            "high": [105, 120, 135, 150, 165],
            "low": [95, 110, 125, 140, 155],
            "close": [115, 130, 145, 160, 175],
            "volume": [15000] * 5
        }, index=idx_higher)

    def _worker_task(self, worker_id: int):
        """Worker task to run engines concurrently and return deterministic fingerprint."""
        # 1. Normalize
        norm_lower = self.norm_engine.normalize(self.raw_lower.copy(), symbol=f"SYM_{worker_id}", timeframe="1m")
        norm_higher = self.norm_engine.normalize(self.raw_higher.copy(), symbol=f"SYM_{worker_id}", timeframe="15m")
        
        # 2. Align
        aligned = self.mtf_engine.align(norm_lower, norm_higher)
        
        # 3. Hash to guarantee deterministic output
        fingerprint = pd.util.hash_pandas_object(aligned).sum()
        return fingerprint

    def test_concurrent_execution(self):
        """Tests that spawning 8 threads produces perfectly deterministic outputs with no race conditions."""
        threads = 8
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(self._worker_task, i) for i in range(threads)]
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
                
        # Assert exactly 8 results
        assert len(results) == threads
        
        # Assert all results are IDENTICAL (deterministic)
        assert len(set(results)) == 1
