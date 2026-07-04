from typing import Dict, Any
from Backend.indicator_engine.registry import IndicatorRegistry

class IndicatorFactory:
    """Instantiates and caches Indicator Engines."""
    _cache: Dict[str, Any] = {}
    
    @classmethod
    def get_instance(cls, indicator_id: str, **kwargs) -> Any:
        # Create a cache key based on ID and parameters
        # Sort kwargs to ensure consistent keys
        sorted_kwargs = tuple(sorted(kwargs.items()))
        cache_key = f"{indicator_id}_{hash(sorted_kwargs)}"
        
        if cache_key in cls._cache:
            return cls._cache[cache_key]
            
        registration = IndicatorRegistry.get(indicator_id)
        if not registration:
            raise ValueError(f"Indicator '{indicator_id}' is not registered in IndicatorRegistry.")
            
        engine_class = registration["engine"]
        instance = engine_class(**kwargs)
        
        cls._cache[cache_key] = instance
        return instance
    
    @classmethod
    def clear_cache(cls):
        cls._cache.clear()
