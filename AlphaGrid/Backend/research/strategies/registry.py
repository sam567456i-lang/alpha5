"""Strategy Registry."""

import threading
from typing import Dict, List
from Backend.research.strategies.definition import StrategyDefinition

class StrategyRegistry:
    """Registry for purely declarative StrategyDefinitions."""
    
    _definitions: Dict[str, StrategyDefinition] = {}
    _lock = threading.Lock()

    @classmethod
    def register(cls, definition: StrategyDefinition) -> None:
        """Register a new strategy definition with full validation."""
        # 1. Unique ID
        with cls._lock:
            if definition.id in cls._definitions:
                raise ValueError(f"StrategyDefinition with ID {definition.id} is already registered.")
                
            # 2. Validate Family Assignment
            if not definition.methodology:
                raise ValueError(f"Strategy {definition.id} must declare a Methodology (Family).")
                
            # 3. Validate Dependencies
            if not definition.features and not definition.concepts and not definition.primitive_signals:
                raise ValueError(f"Strategy {definition.id} declares no dependencies. Placeholders are prohibited.")
                
            # 4. Parameter Schema (Basic check)
            if not isinstance(definition.parameters, dict):
                raise ValueError(f"Strategy {definition.id} parameters must be a dictionary.")
                
            cls._definitions[definition.id] = definition

    @classmethod
    def get(cls, strategy_id: str) -> StrategyDefinition:
        """Retrieve a strategy definition by ID."""
        with cls._lock:
            if strategy_id not in cls._definitions:
                raise KeyError(f"StrategyDefinition with ID {strategy_id} not found.")
            return cls._definitions[strategy_id]

    @classmethod
    def get_all(cls) -> List[StrategyDefinition]:
        """Retrieve all registered strategy definitions."""
        with cls._lock:
            return list(cls._definitions.values())
        
    @classmethod
    def clear(cls) -> None:
        """Clear all definitions (primarily for testing)."""
        with cls._lock:
            cls._definitions.clear()
