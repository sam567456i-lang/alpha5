import pytest
import numpy as np
import pandas as pd
from Backend.features.support_resistance import SupportResistanceFeatureGenerator
from Backend.features.high_low_breakout import HighLowBreakoutFeatureGenerator
from Backend.features.volatility_breakout import VolatilityBreakoutFeatureGenerator
from Backend.concepts.core.breakout import BreakoutConceptGenerator
from Backend.methodologies.breakout import BreakoutMethodology
from Backend.signals.primitive.generators.breakout_signals import BreakoutPrimitiveSignalGenerator


@pytest.fixture
def sample_data():
    np.random.seed(42)
    dates = pd.date_range(start='2026-01-01', periods=100, freq='D')
    df = pd.DataFrame({
        'open': np.random.uniform(100, 110, 100),
        'high': np.random.uniform(110, 120, 100),
        'low': np.random.uniform(90, 100, 100),
        'close': np.random.uniform(95, 115, 100),
        'volume': np.random.uniform(1000, 5000, 100),
    }, index=dates)
    df.attrs['symbol'] = 'TEST/USD'
    df.attrs['timeframe'] = '1d'
    return df


# --- Feature Determinism ---

def test_sr_determinism(sample_data):
    gen = SupportResistanceFeatureGenerator(lookback=20)
    dto1 = gen.generate(sample_data, "trc-1", "cor-1")
    dto2 = gen.generate(sample_data, "trc-2", "cor-2")
    assert dto1.values['resistance'] == dto2.values['resistance']
    assert dto1.values['support'] == dto2.values['support']
    assert dto1.checksum == dto2.checksum


def test_hl_breakout_determinism(sample_data):
    gen = HighLowBreakoutFeatureGenerator(period=20)
    dto1 = gen.generate(sample_data, "trc-1", "cor-1")
    dto2 = gen.generate(sample_data, "trc-2", "cor-2")
    assert dto1.values['high_breakout'] == dto2.values['high_breakout']
    assert dto1.values['low_breakout'] == dto2.values['low_breakout']
    assert dto1.checksum == dto2.checksum


def test_vol_breakout_determinism(sample_data):
    gen = VolatilityBreakoutFeatureGenerator(atr_period=14, multiplier=1.5)
    dto1 = gen.generate(sample_data, "trc-1", "cor-1")
    dto2 = gen.generate(sample_data, "trc-2", "cor-2")
    assert dto1.values['upside_breakout'] == dto2.values['upside_breakout']
    assert dto1.values['downside_breakout'] == dto2.values['downside_breakout']
    assert dto1.checksum == dto2.checksum


# --- Concept Determinism ---

def test_breakout_concept_determinism(sample_data):
    sr_gen = SupportResistanceFeatureGenerator(lookback=20)
    hl_gen = HighLowBreakoutFeatureGenerator(period=20)
    sr_dto = sr_gen.generate(sample_data, "trc-1", "cor-1")
    hl_dto = hl_gen.generate(sample_data, "trc-1", "cor-1")

    concept_gen = BreakoutConceptGenerator()
    c1 = concept_gen.generate([sr_dto, hl_dto], "trc-1", "cor-1")
    c2 = concept_gen.generate([sr_dto, hl_dto], "trc-2", "cor-2")
    assert c1.state == c2.state
    assert c1.checksum == c2.checksum


# --- Methodology Determinism ---

def test_breakout_methodology_determinism(sample_data):
    sr_gen = SupportResistanceFeatureGenerator(lookback=20)
    sr_dto = sr_gen.generate(sample_data, "trc-1", "cor-1")

    concept_gen = BreakoutConceptGenerator()
    concept = concept_gen.generate([sr_dto], "trc-1", "cor-1")

    meth = BreakoutMethodology()
    m1 = meth.evaluate(concept, trace_id="trc-1", correlation_id="cor-1")
    m2 = meth.evaluate(concept, trace_id="trc-2", correlation_id="cor-2")
    assert m1.is_active == m2.is_active
    assert m1.direction == m2.direction
    assert m1.checksum == m2.checksum


# --- Signal Determinism ---

def test_breakout_signal_determinism(sample_data):
    sr_gen = SupportResistanceFeatureGenerator(lookback=20)
    sr_dto = sr_gen.generate(sample_data, "trc-1", "cor-1")
    concept = BreakoutConceptGenerator().generate([sr_dto], "trc-1", "cor-1")
    meth = BreakoutMethodology().evaluate(concept, trace_id="trc-1", correlation_id="cor-1")

    sig_gen = BreakoutPrimitiveSignalGenerator()
    s1 = sig_gen.generate(meth, "trc-1", "cor-1")
    s2 = sig_gen.generate(meth, "trc-2", "cor-2")
    assert s1.signal_type == s2.signal_type
    assert s1.checksum == s2.checksum


# --- Full Pipeline Integration ---

def test_full_breakout_pipeline(sample_data):
    """End-to-end pipeline: Feature -> Concept -> Methodology -> Signal -> Strategy."""
    from Backend.strategy.strategies.breakout_strategies import SRBreakoutStrategy

    sr_dto = SupportResistanceFeatureGenerator(lookback=20).generate(sample_data, "trc-1", "cor-1")
    hl_dto = HighLowBreakoutFeatureGenerator(period=20).generate(sample_data, "trc-1", "cor-1")

    concept = BreakoutConceptGenerator().generate([sr_dto, hl_dto], "trc-1", "cor-1")
    meth = BreakoutMethodology().evaluate(concept, trace_id="trc-1", correlation_id="cor-1")
    signal = BreakoutPrimitiveSignalGenerator().generate(meth, "trc-1", "cor-1")
    strat = SRBreakoutStrategy(sr_lookback=20).generate(signal, "trc-1", "cor-1")

    assert strat.action in ("BUY", "SELL", "HOLD")
    assert strat.metadata['strategy_metadata']['family'] == "Breakout"
    assert strat.schema_version == "1.0.0"
