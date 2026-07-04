from typing import Dict, Any, Type, Optional

class IndicatorRegistry:
    """Python-based runtime registry for Indicator Engines."""
    _registry: Dict[str, Dict[str, Any]] = {}
    
    @classmethod
    def register(cls, id: str, engine_class: Type, result_class: Type):
        cls._registry[id] = {
            "engine": engine_class,
            "result": result_class
        }
        
    @classmethod
    def get(cls, id: str) -> Optional[Dict[str, Any]]:
        return cls._registry.get(id)
        
    @classmethod
    def get_all(cls) -> Dict[str, Dict[str, Any]]:
        return cls._registry.copy()
