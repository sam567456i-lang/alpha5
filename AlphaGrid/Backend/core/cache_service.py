from typing import Any, Dict

class CacheService:
    """Stub CacheService for testing"""
    def __init__(self):
        self.cache: Dict[str, Any] = {}
        
    def get(self, key: str) -> Any:
        return self.cache.get(key)
        
    def set(self, key: str, value: Any):
        self.cache[key] = value
