"""Integration tests for Declarative Strategy Framework."""

import pytest
from Backend.research.strategies.definition import StrategyDefinition
from Backend.research.strategies.registry import StrategyRegistry
from Backend.research.strategies.factory import StrategyFactory
from Backend.research.strategies.definitions.rsi_reversion import RSI_REVERSION
from Backend.research.strategies.definitions.bollinger_reversion import BOLLINGER_REVERSION
from Backend.research.strategies.definitions.supertrend_cross import SUPERTREND_CROSS

from Backend.research.strategies.base_research_strategy import BaseResearchStrategy
from Backend.concepts.generators.trend import TrendConceptGenerator
from Backend.signals.primitive.generators.extremum import OverextendedSignalGenerator
from Backend.signals.primitive.generators.trend import StrongTrendSignalGenerator

from Backend.research.strategies.definitions.macd_momentum import MACD_MOMENTUM
from Backend.research.strategies.definitions.exhaustion_reversal import EXHAUSTION_REVERSAL
from Backend.research.strategies.definitions.relative_volume_surge import RELATIVE_VOLUME_SURGE
from Backend.research.strategies.definitions.volatility_expansion import VOLATILITY_EXPANSION

from Backend.features.macd import MACDHistogramFeature
from Backend.features.relative_volume import RelativeVolumeFeature
from Backend.features.bollinger import BollingerBandsFeature
from Backend.features.supertrend import SuperTrendFeature
from Backend.research.strategies.definitions.ema_cross import EMA_CROSS
from Backend.research.strategies.definitions.sma_cross import SMA_CROSS
from Backend.research.strategies.definitions.roc_momentum import ROC_MOMENTUM
from Backend.research.strategies.definitions.stochastic_reversion import STOCHASTIC_REVERSION
from Backend.research.strategies.definitions.donchian_trend import DONCHIAN_TREND
from Backend.research.strategies.definitions.keltner_reversion import KELTNER_REVERSION
from Backend.research.strategies.definitions.cci_reversion import CCI_REVERSION
from Backend.research.strategies.definitions.stochastic_momentum import STOCHASTIC_MOMENTUM
from Backend.research.strategies.definitions.stochastic_exhaustion import STOCHASTIC_EXHAUSTION

from Backend.features.trend import EMAFeature, SMAFeature
from Backend.features.momentum import ROCFeature, RSIFeature
from Backend.features.stochastic import StochasticFeature
from Backend.features.donchian import Donchian20Feature
from Backend.features.keltner import KeltnerChannelFeature
from Backend.features.cci import CCIFeature
from Backend.features.volatility import ATRFeature

def test_strategy_registry():
    StrategyRegistry.clear()
    
    StrategyRegistry.register(RSI_REVERSION)
    StrategyRegistry.register(BOLLINGER_REVERSION)
    StrategyRegistry.register(SUPERTREND_CROSS)
    StrategyRegistry.register(MACD_MOMENTUM)
    StrategyRegistry.register(EXHAUSTION_REVERSAL)
    StrategyRegistry.register(RELATIVE_VOLUME_SURGE)
    StrategyRegistry.register(VOLATILITY_EXPANSION)
    StrategyRegistry.register(EMA_CROSS)
    StrategyRegistry.register(SMA_CROSS)
    StrategyRegistry.register(ROC_MOMENTUM)
    StrategyRegistry.register(STOCHASTIC_REVERSION)
    StrategyRegistry.register(DONCHIAN_TREND)
    StrategyRegistry.register(KELTNER_REVERSION)
    StrategyRegistry.register(CCI_REVERSION)
    StrategyRegistry.register(STOCHASTIC_MOMENTUM)
    StrategyRegistry.register(STOCHASTIC_EXHAUSTION)
    
    assert len(StrategyRegistry.get_all()) == 16
    assert StrategyRegistry.get("STRAT-MOM-001") == MACD_MOMENTUM
    assert StrategyRegistry.get("STRAT-TRND-001") == EMA_CROSS
    
    with pytest.raises(ValueError):
        StrategyRegistry.register(RSI_REVERSION) # Duplicate ID

def test_strategy_factory_instantiation():
    """Verify that the declarative definitions successfully hydrate into executable BaseResearchStrategy instances."""
    
    # Test RSI
    rsi_strat = StrategyFactory.create(RSI_REVERSION)
    assert isinstance(rsi_strat, BaseResearchStrategy)
    assert RSIFeature in rsi_strat.config.features
    
    # Test Bollinger
    boll_strat = StrategyFactory.create(BOLLINGER_REVERSION)
    assert isinstance(boll_strat, BaseResearchStrategy)
    assert BollingerBandsFeature in boll_strat.config.features
    
    # Test SuperTrend
    st_strat = StrategyFactory.create(SUPERTREND_CROSS)
    assert isinstance(st_strat, BaseResearchStrategy)
    assert SuperTrendFeature in st_strat.config.features

    # Test Momentum
    mom_strat = StrategyFactory.create(MACD_MOMENTUM)
    assert isinstance(mom_strat, BaseResearchStrategy)
    assert MACDHistogramFeature in mom_strat.config.features

    # Test Reversal
    rev_strat = StrategyFactory.create(EXHAUSTION_REVERSAL)
    assert isinstance(rev_strat, BaseResearchStrategy)
    assert RSIFeature in rev_strat.config.features

    # Test Volume
    vol_strat = StrategyFactory.create(RELATIVE_VOLUME_SURGE)
    assert isinstance(vol_strat, BaseResearchStrategy)
    assert RelativeVolumeFeature in vol_strat.config.features

    # Test Volatility
    vola_strat = StrategyFactory.create(VOLATILITY_EXPANSION)
    assert isinstance(vola_strat, BaseResearchStrategy)
    assert BollingerBandsFeature in vola_strat.config.features

def test_end_to_end_scientific_evaluation():
    """Verify every registered strategy hydrates and executes Scientific Evaluation."""
    from Backend.research.evaluation.evaluator import ScientificEvaluator
    from Backend.research.evaluation.policy import PromotionPolicy
    
    # We will clear and re-register all strategies to ensure the registry is populated for this test.
    test_strategy_registry()
    
    # Create an evaluator with a minimal policy to ensure it doesn't fail on mock data
    policy = PromotionPolicy(min_trades=5, min_sharpe=0.5)
    evaluator = ScientificEvaluator(policy=policy)
    
    # Mock data for evaluation
    pnls = [10.0, 12.0, 8.0, 15.0, 5.0, 20.0]
    trades = [{"pnl": p} for p in pnls]
    equity_curve = [1000.0 + i*10 for i in range(11)]
    
    all_strategies = StrategyRegistry.get_all()
    assert len(all_strategies) > 0, "Registry is empty!"
    
    for definition in all_strategies:
        # 1. Hydrate
        strategy = StrategyFactory.create(definition)
        assert isinstance(strategy, BaseResearchStrategy)
        
        # 2. Dependency check happens implicitly during hydration, 
        # but let's verify features exist.
        assert len(strategy.config.features) > 0
        
        # 3. Scientific Evaluation
        report = evaluator.evaluate(
            experiment_id=f"EXP_{definition.id}",
            hypothesis_id=definition.research_hypothesis_id or "RH_MOCK",
            trades=trades,
            equity_curve=equity_curve
        )
        
        # 4. Evaluation Report check
        assert report is not None
        assert report.experiment_id == f"EXP_{definition.id}"
        # It should promote based on our mock data and minimal policy
        assert report.is_promoted is True

