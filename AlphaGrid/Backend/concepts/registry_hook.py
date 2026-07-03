"""Dependency Injection registry hook for the Concept domain."""

import importlib
import pkgutil
import inspect
from Backend.foundation.dependency_injection_container import DependencyContainer
from Backend.concepts.registry import ConceptRegistry
from Backend.concepts.engine import ConceptEngine
from Backend.concepts.generator import AbstractConceptGenerator

def register_concepts(container: DependencyContainer) -> None:
    """
    Registers the Concept domain components into the DI container.
    Auto-discovers and mounts all concept plugins.
    """
    registry = ConceptRegistry()
    
    from Backend.concepts.generators.breakout import BreakoutConceptGenerator
    from Backend.concepts.generators.extremum import ExtremumConceptGenerator, ThresholdConfig
    from Backend.concepts.generators.momentum import MomentumConceptGenerator
    from Backend.concepts.generators.strength import StrengthConceptGenerator, StrengthThresholdConfig
    from Backend.concepts.generators.trend import TrendConceptGenerator
    from Backend.concepts.generators.volatility import VolatilityConceptGenerator
    from Backend.concepts.generators.volume import VolumeConceptGenerator
    
    # Phase 10D: Market Structure Concepts
    from Backend.concepts.generators.price_action import PriceActionConceptGenerator
    from Backend.concepts.generators.market_structure import MarketStructureConceptGenerator
    from Backend.concepts.generators.wyckoff import WyckoffConceptGenerator
    
    # Manually register the required baseline concepts instead of failing auto-discovery
    registry.register(BreakoutConceptGenerator(source="close"))
    registry.register(ExtremumConceptGenerator(source="close", config=ThresholdConfig(upper=70.0, lower=30.0)))
    registry.register(MomentumConceptGenerator(source="close"))
    registry.register(StrengthConceptGenerator(source="close", config=StrengthThresholdConfig()))
    registry.register(TrendConceptGenerator(source="close"))
    registry.register(VolatilityConceptGenerator(source="close"))
    registry.register(VolumeConceptGenerator(source="volume"))
    
    # Register Phase 10D generators
    registry.register(PriceActionConceptGenerator())
    registry.register(MarketStructureConceptGenerator())
    registry.register(WyckoffConceptGenerator())
                
    # Mount into DI container as singletons
    container.register_factory("concept_registry", lambda c: registry, singleton=True)
    container.register_factory("concept_engine", lambda c: ConceptEngine(registry=registry), singleton=True)
