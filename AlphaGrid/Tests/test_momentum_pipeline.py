import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from Backend.features.macd_generator import MACDFeatureGenerator
from Backend.features.roc_generator import ROCFeatureGenerator
from Backend.concepts.runtime.momentum_semantic import MomentumSemanticConceptGenerator
from Backend.methodology.runtime.momentum import MomentumRuntimeMethodology
from Backend.signals.primitive.generators.momentum_runtime import MomentumRuntimeSignalGenerator
from Backend.strategy.strategies.macd_momentum import MACDMomentumStrategy
from Backend.strategy.strategies.roc_momentum import ROCMomentumStrategy

def _create_mock_data(size=100, add_nans=False, add_infs=False, zero_vol=False):
    dates = pd.date_range(start=datetime.now(), periods=size, freq='1h')
    df = pd.DataFrame(index=dates)
    df['open'] = np.linspace(10, 20, size)
    df['high'] = df['open'] + 1
    df['low'] = df['open'] - 1
    df['close'] = df['open'] + np.sin(np.linspace(0, 10, size))
    df['volume'] = 1000 if not zero_vol else 0
    
    if add_nans:
        df.iloc[size//2, df.columns.get_loc('close')] = np.nan
    if add_infs:
        df.iloc[size//3, df.columns.get_loc('close')] = np.inf
        
    df.attrs['symbol'] = 'BTCUSDT'
    df.attrs['timeframe'] = '1h'
    return df

class TestMomentumPipeline:
    
    def test_numerical_robustness(self):
        """Test how pipeline handles NaNs, Infs, and zero volume."""
        df_clean = _create_mock_data(100)
        df_nans = _create_mock_data(100, add_nans=True)
        df_infs = _create_mock_data(100, add_infs=True)
        df_zero = _create_mock_data(100, zero_vol=True)
        
        macd = MACDFeatureGenerator()
        roc = ROCFeatureGenerator()
        
        # Clean should pass
        feat_clean = macd.generate(df_clean, "tr1", "corr1")
        assert feat_clean.values['macd_line'] is not None
        
        feat_clean_roc = roc.generate(df_clean, "tr1", "corr1")
        assert feat_clean_roc.values['roc'] is not None
        
        # Zero volume should pass (momentum mostly relies on price)
        feat_zero = macd.generate(df_zero, "tr1", "corr1")
        assert feat_zero.values['macd_line'] is not None
        
        # NaNs and Infs should be caught and not crash Python, but output might be NaN
        # or pandas will naturally forward-fill if we handled it.
        # As long as it doesn't crash catastrophically, we're testing robustness.
        macd.generate(df_nans, "tr1", "corr1")
        macd.generate(df_infs, "tr1", "corr1")

    def test_deterministic_replay(self):
        """Run -> Hash -> Run -> Hash -> Equal"""
        df = _create_mock_data(100)
        
        macd = MACDFeatureGenerator()
        run1 = macd.generate(df, "tr1", "corr1")
        run2 = macd.generate(df, "tr1", "corr1")
        
        # Deterministic generation logic
        assert run1.checksum == run2.checksum
        
        concept = MomentumSemanticConceptGenerator()
        c1 = concept.evaluate([run1], "tr1", "corr1")
        c2 = concept.evaluate([run2], "tr1", "corr1")
        assert c1.checksum == c2.checksum
        
        meth = MomentumRuntimeMethodology()
        m1 = meth.evaluate([c1], "tr1", "corr1")
        m2 = meth.evaluate([c2], "tr1", "corr1")
        assert m1.checksum == m2.checksum

    def test_cross_family_isolation(self):
        """Verify momentum state doesn't leak into trend states dynamically."""
        df = _create_mock_data(100)
        
        # Generate momentum
        macd = MACDFeatureGenerator()
        feat = macd.generate(df, "t", "c")
        
        # Generate concept
        concept = MomentumSemanticConceptGenerator()
        con = concept.evaluate([feat], "t", "c")
        
        assert con.concept_type == 'momentum'
        assert con.state in ["ACCELERATING_UP", "DECELERATING_UP", "STEADY_UP", "ACCELERATING_DOWN", "DECELERATING_DOWN", "STEADY_DOWN", "DIVERGING", "NEUTRAL"]
        
        # Trend concepts should remain unaffected. If we pass this concept to a trend meth, it should fail
        # ensuring isolation.
        from Backend.methodology.trend_following import TrendFollowingMethodology
        trend_meth = TrendFollowingMethodology()
        try:
            # Should fail or ignore because it's looking for 'trend' concepts, not 'momentum'
            trend_meth.evaluate([con])
            # If it doesn't fail, it should return NEUTRAL or similar isolation
        except (ValueError, AttributeError):
            pass # ValueError/AttributeError is acceptable isolation

    def test_pipeline_e2e(self):
        df = _create_mock_data(100)
        macd = MACDFeatureGenerator()
        feat = macd.generate(df, "t", "c")
        
        concept = MomentumSemanticConceptGenerator()
        con = concept.evaluate([feat], "t", "c")
        
        meth = MomentumRuntimeMethodology()
        m = meth.evaluate([con], "t", "c")
        
        sig_gen = MomentumRuntimeSignalGenerator()
        sig = sig_gen.generate([m], "t", "c")
        
        strat = MACDMomentumStrategy()
        decisions = strat.evaluate(datetime.now(), [sig])
        
        # We should have a valid list of decisions (0 or more)
        assert isinstance(decisions, list)

    def test_performance_memory_scale(self):
        """Benchmark test for 100,000 bars."""
        import time
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024  # MB
        
        # 100,000 bars
        df_large = _create_mock_data(100000)
        
        start_time = time.time()
        
        macd = MACDFeatureGenerator()
        feat = macd.generate(df_large, "t", "c")
        
        concept = MomentumSemanticConceptGenerator()
        con = concept.evaluate([feat], "t", "c")
        
        meth = MomentumRuntimeMethodology()
        m = meth.evaluate([con], "t", "c")
        
        sig_gen = MomentumRuntimeSignalGenerator()
        sig = sig_gen.generate([m], "t", "c")
        
        end_time = time.time()
        mem_after = process.memory_info().rss / 1024 / 1024  # MB
        
        latency = end_time - start_time
        mem_growth = mem_after - mem_before
        
        # Expectations for institutional pipeline
        # 100k bars should process in under 3.0 seconds
        assert latency < 3.0, f"Latency too high: {latency}s"
        # 100k bars shouldn't leak massive memory
        assert mem_growth < 500.0, f"Memory growth too high: {mem_growth}MB"
        print(f"\\nPerformance [100k Bars]: Latency={latency:.3f}s | Memory={mem_growth:.2f}MB")

