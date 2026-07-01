"""Research execution engine components."""

from .dataset_loader import DatasetLoader, DatasetIntegrityError
from .strategy_interface import AbstractStrategy, STRATEGY_REGISTRY, StrategyRegistry
from .backtest import BacktestEngine

__all__ = [
    "DatasetLoader",
    "DatasetIntegrityError",
    "AbstractStrategy",
    "STRATEGY_REGISTRY",
    "StrategyRegistry",
    "BacktestEngine",
]
