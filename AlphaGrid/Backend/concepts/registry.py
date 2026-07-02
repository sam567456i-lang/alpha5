"""Concept Registry."""

from typing import Dict, List
from .generator import AbstractConceptGenerator


class ConceptRegistry:
    """Registers Concept Generators."""

    def __init__(self) -> None:
        self._generators: Dict[str, AbstractConceptGenerator] = {}

    def register(self, generator: AbstractConceptGenerator) -> None:
        if not isinstance(generator, AbstractConceptGenerator):
            raise TypeError("Must be an instance of AbstractConceptGenerator")
            
        cid = generator.get_id()
        if cid in self._generators:
            raise ValueError(f"Duplicate concept ID: '{cid}'")
            
        self._generators[cid] = generator

    def get_all(self) -> List[AbstractConceptGenerator]:
        return list(self._generators.values())

    def clear(self) -> None:
        self._generators.clear()
