"""Concept Registry."""

from typing import Type, Dict, List
from .generator import AbstractConceptGenerator


class ConceptRegistry:
    """Registers AbstractConceptGenerators."""

    def __init__(self) -> None:
        self._generators: Dict[str, Type[AbstractConceptGenerator]] = {}

    def register(self, generator_cls: Type[AbstractConceptGenerator]) -> None:
        if not issubclass(generator_cls, AbstractConceptGenerator):
            raise TypeError(f"{generator_cls.__name__} must inherit from AbstractConceptGenerator")
            
        cid = generator_cls.get_id()
        if cid in self._generators:
            raise ValueError(f"Duplicate concept ID: '{cid}'")
            
        self._generators[cid] = generator_cls

    def get_all(self) -> List[Type[AbstractConceptGenerator]]:
        return list(self._generators.values())

    def clear(self) -> None:
        self._generators.clear()
