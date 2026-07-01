"""Strategy interface and registry for the Research Platform (ADP Sec 10)."""

from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any, Dict, Type
import re

STRATEGY_ID_REGEX = re.compile(r"^[A-Z0-9_]+$")


class AbstractStrategy(ABC):
    """Base class for all research strategies to guarantee event-driven compliance."""

    @classmethod
    def get_parameter_schema(cls) -> Dict[str, Dict[str, Any]]:
        """
        Returns the parameter schema for validation.
        Format: {
            "param_name": {
                "type": type,
                "required": bool,
                "default": Any,
                "min": Any,
                "max": Any
            }
        }
        """
        return {}

    @classmethod
    def max_label_horizon(cls) -> timedelta:
        """
        Returns the maximum forward-looking label horizon for this strategy.
        Purely reactive strategies (e.g., EMA crossover) return timedelta(0).
        ML strategies using N-bar-forward returns MUST override this to declare
        their actual lookahead window, which the WalkForwardEngine uses to
        enforce the embargo period between IS and OOS boundaries.
        """
        return timedelta(0)

    def __init__(self, parameters: Dict[str, Any], random_generator: Any) -> None:
        """
        Initializes the strategy.
        Args:
            parameters: The deterministic JSON-validated parameters.
            random_generator: The root seeded numpy PCG64 generator.
        """
        self.parameters = parameters
        self.rng = random_generator

    @abstractmethod
    def on_market_event(self, event: Dict[str, Any]) -> None:
        """
        Invoked chronologically on every market data event.
        Must not contain lookahead bias.
        """
        pass


class StrategyRegistry:
    """Manages strategy resolution and validation."""

    def __init__(self) -> None:
        self._registry: Dict[str, Type[AbstractStrategy]] = {}

    def register(self, strategy_id: str, strategy_cls: Type[AbstractStrategy]) -> None:
        """Registers a strategy class against an immutable ID."""
        if not STRATEGY_ID_REGEX.match(strategy_id):
            raise ValueError(f"Invalid strategy ID '{strategy_id}'. Must match ^[A-Z0-9_]+$")
        if strategy_id in self._registry:
            raise ValueError(f"Duplicate strategy ID '{strategy_id}'. Already registered.")
        if not issubclass(strategy_cls, AbstractStrategy):
            raise TypeError(f"Strategy {strategy_cls.__name__} must inherit from AbstractStrategy")
        self._registry[strategy_id] = strategy_cls

    def get_strategy(self, strategy_id: str) -> Type[AbstractStrategy]:
        """Resolves a strategy ID to its class."""
        if strategy_id not in self._registry:
            raise ValueError(f"Unknown strategy ID '{strategy_id}'.")
        return self._registry[strategy_id]

# Global immutable registry mapped at startup
STRATEGY_REGISTRY = StrategyRegistry()
