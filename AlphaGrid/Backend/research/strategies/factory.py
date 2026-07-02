"""Strategy Factory."""

from typing import Any
import numpy as np

from Backend.research.strategies.definition import StrategyDefinition
from Backend.research.strategies.config import StrategyConfig
from Backend.research.strategies.base_research_strategy import BaseResearchStrategy

class StrategyFactory:
    """Dynamically constructs configured BaseResearchStrategy instances from declarative definitions."""

    @staticmethod
    def create(definition: StrategyDefinition, random_generator: Any = None) -> BaseResearchStrategy:
        """
        Instantiate a strategy from its definition.
        
        Args:
            definition: The declarative strategy definition.
            random_generator: Optional numpy random generator for stochastic behaviors.
            
        Returns:
            An instantiated and configured BaseResearchStrategy.
        """
        if random_generator is None:
            random_generator = np.random.Generator(np.random.PCG64())

        # Instantiate Concept Generators
        concept_generators = []
        for c_def in definition.concepts:
            gen = c_def.generator_type(source=c_def.source, **c_def.kwargs)  # type: ignore
            concept_generators.append(gen)
            
        # Instantiate Primitive Signal Generators
        ps_generators = [ps_def.generator_type() for ps_def in definition.primitive_signals]

        # Instantiate Methodology
        methodologies = [definition.methodology()]

        # Build Config
        config = StrategyConfig(
            features=definition.features,
            concept_generators=concept_generators,
            primitive_signal_generators=ps_generators,
            methodologies=methodologies
        )

        # Instantiate the final strategy wrapper
        return definition.strategy_class(
            parameters=definition.parameters,
            random_generator=random_generator,
            config=config
        )
