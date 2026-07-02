"""Strategy implementations."""

from .base_research_strategy import BaseResearchStrategy
from .config import StrategyConfig

from .registry import StrategyRegistry

def register_all_strategies() -> None:
    """Hydrate the strategy registry with all declarative definitions."""
    from .definitions.rsi_reversion import RSI_REVERSION
    from .definitions.bollinger_reversion import BOLLINGER_REVERSION
    from .definitions.supertrend_cross import SUPERTREND_CROSS
    from .definitions.macd_momentum import MACD_MOMENTUM
    from .definitions.exhaustion_reversal import EXHAUSTION_REVERSAL
    from .definitions.relative_volume_surge import RELATIVE_VOLUME_SURGE
    from .definitions.volatility_expansion import VOLATILITY_EXPANSION
    from .definitions.ema_cross import EMA_CROSS
    from .definitions.sma_cross import SMA_CROSS
    from .definitions.roc_momentum import ROC_MOMENTUM
    from .definitions.stochastic_reversion import STOCHASTIC_REVERSION
    from .definitions.donchian_trend import DONCHIAN_TREND
    from .definitions.keltner_reversion import KELTNER_REVERSION
    from .definitions.cci_reversion import CCI_REVERSION
    from .definitions.stochastic_momentum import STOCHASTIC_MOMENTUM
    from .definitions.stochastic_exhaustion import STOCHASTIC_EXHAUSTION

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

__all__ = [
    'BaseResearchStrategy',
    'StrategyConfig',
    'register_all_strategies'
]
