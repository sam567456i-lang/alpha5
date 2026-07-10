from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime

@dataclass(frozen=True)
class MethodologyContext:
    """
    Immutable snapshot of the market environment at a specific evaluation cycle.
    Methodologies evaluate this context rather than polling engines dynamically.
    """
    context_id: str
    symbol: str
    timeframe: str
    execution_timestamp: datetime
    market_regime: str
    available_capabilities: List[str]
    object_graph_snapshot: Dict[str, Any]  # UUID -> BasePlatformObject
    feature_snapshot: Dict[str, float]      # FeatureID -> NormalizedValue
    data_quality_score: float
    degradation_state: str

@dataclass(frozen=True)
class MethodologyDefinition:
    """The immutable root methodology research artifact (e.g., SMC)."""
    methodology_id: str
    name: str
    description: str

@dataclass(frozen=True)
class MethodologyVersion:
    """A specific version of a methodology definition (e.g., v2.1)."""
    definition: MethodologyDefinition
    version_id: str
    rule_version: str

@dataclass
class MethodologyInstance:
    """The active execution node bound to a specific runtime environment."""
    instance_id: str
    version: MethodologyVersion
    symbol: str
    timeframe: str
    
    def evaluate(self, context: MethodologyContext) -> Any:
        """Abstract evaluation logic. Must be implemented by concrete profiles."""
        raise NotImplementedError("Methodology must implement evaluate()")

class MethodologySession:
    """Orchestrates one evaluation cycle for a symbol/timeframe across multiple instances."""
    def __init__(self, symbol: str, timeframe: str):
        self.symbol = symbol
        self.timeframe = timeframe
        self.instances: List[MethodologyInstance] = []
        
    def register_instance(self, instance: MethodologyInstance):
        if instance.symbol == self.symbol and instance.timeframe == self.timeframe:
            self.instances.append(instance)
            
    def execute_cycle(self, context: MethodologyContext) -> List[Any]:
        results = []
        for instance in self.instances:
            results.append(instance.evaluate(context))
        return results
