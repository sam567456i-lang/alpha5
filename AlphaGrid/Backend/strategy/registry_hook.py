"""Dependency Injection registry hook for the Strategy domain."""

from Backend.foundation.dependency_injection_container import DependencyContainer
from Backend.strategy.engine import StrategyEngine

def register_strategies(container: DependencyContainer) -> None:
    """
    Registers the Strategy domain components into the DI container.
    """
    container.register_factory("strategy_engine", lambda c: StrategyEngine(), singleton=True)
