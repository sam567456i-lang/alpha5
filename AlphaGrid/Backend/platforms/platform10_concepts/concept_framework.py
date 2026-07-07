"""
Platform 10: Concept Platform - Framework
Orchestrates the execution of Concept Plugins.
"""
from typing import List, Dict, Type
from Backend.platforms.platform10_concepts.concept_base import BaseConcept
from Backend.platforms.platform9_features.feature_base import BaseFeature
from Backend.platforms.platform10_concepts.concept_registry import ConceptRegistry, ConceptPlugin
from Backend.core.state import ExecutionContext

class ConceptCompiler:
    """
    Compiles BaseFeature instances into BaseConcept instances using registered plugins.
    """
    
    def __init__(self):
        self.plugins: List[Type[ConceptPlugin]] = ConceptRegistry.list_plugins()
        
    def compile(self, features: List[BaseFeature], context: ExecutionContext) -> List[BaseConcept]:
        """
        Executes all registered concept plugins against the provided features.
        
        Args:
            features: A list of BaseFeature instances from Platform 9.
            context: The current execution context for generated concepts.
            
        Returns:
            A list of generated BaseConcept instances.
        """
        concepts = []
        for plugin_cls in self.plugins:
            # Instantiate the plugin and extract concepts
            plugin_instance = plugin_cls()
            extracted_concepts = plugin_instance.extract(features, context)
            
            # Freeze and validate concepts
            for concept in extracted_concepts:
                if not isinstance(concept, BaseConcept):
                    raise TypeError(f"Plugin {plugin_cls.__name__} returned non-BaseConcept: {type(concept)}")
                
                # Enforce context propagation
                if concept.context != context:
                    raise ValueError(f"Plugin {plugin_cls.__name__} generated concept with incorrect context.")
                
                concept.freeze()
                concepts.append(concept)
                
        return concepts

# Extend ConceptPlugin to include extract method
def _extract(self, features: List[BaseFeature], context: ExecutionContext) -> List[BaseConcept]:
    """Extracts concepts from features. Must be implemented by subclasses."""
    raise NotImplementedError

ConceptPlugin.extract = _extract
