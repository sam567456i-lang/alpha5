"""
Platform 10: Concept Platform - Registry
Maintains a registry of all available Concept plugins.
"""
from typing import Dict, Type, List, Optional
from Backend.platforms.platform9_concepts.concept_base import ConceptCategory, ConceptType

class ConceptPlugin:
    """Base class for all Concept Plugins."""
    
    @classmethod
    def get_category(cls) -> ConceptCategory:
        raise NotImplementedError
        
    @classmethod
    def get_type(cls) -> ConceptType:
        raise NotImplementedError
        
    @classmethod
    def get_version(cls) -> str:
        return "1.0.0"


class ConceptRegistry:
    """Central registry for all Concept plugins."""
    
    _registry: Dict[str, Type[ConceptPlugin]] = {}
    
    @classmethod
    def register(cls, plugin: Type[ConceptPlugin]) -> Type[ConceptPlugin]:
        """Registers a Concept Plugin."""
        key = f"{plugin.get_category().value}_{plugin.get_type().value}_{plugin.get_version()}"
        if key in cls._registry:
            raise ValueError(f"Concept plugin {key} is already registered.")
        cls._registry[key] = plugin
        return plugin
        
    @classmethod
    def get_plugin(cls, category: ConceptCategory, type_: ConceptType, version: str = "1.0.0") -> Optional[Type[ConceptPlugin]]:
        """Retrieves a registered plugin by its attributes."""
        key = f"{category.value}_{type_.value}_{version}"
        return cls._registry.get(key)
        
    @classmethod
    def list_plugins(cls) -> List[Type[ConceptPlugin]]:
        """Returns a list of all registered plugins."""
        return list(cls._registry.values())

    @classmethod
    def clear(cls) -> None:
        """Clears the registry. Used for testing."""
        cls._registry.clear()
