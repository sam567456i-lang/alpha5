"""Geometry Cache for incremental bar execution."""
from typing import Dict, List, Any, Optional
from Backend.price_geometry.objects import GeometryObject

class GeometryCache:
    """
    Caches geometry objects to avoid recomputation on every new bar.
    Provides fast O(1) lookups by ID and indexed lookups by type/symbol.
    """
    def __init__(self):
        self._cache: Dict[str, GeometryObject] = {}
        self._by_type: Dict[str, List[str]] = {}
        self._by_symbol: Dict[str, List[str]] = {}
        self._last_bar_timestamp: Optional[str] = None
        
    def add(self, obj: GeometryObject) -> None:
        self._cache[obj.id] = obj
        
        type_name = obj.__class__.__name__
        if type_name not in self._by_type:
            self._by_type[type_name] = []
        if obj.id not in self._by_type[type_name]:
            self._by_type[type_name].append(obj.id)
            
        if obj.symbol not in self._by_symbol:
            self._by_symbol[obj.symbol] = []
        if obj.id not in self._by_symbol[obj.symbol]:
            self._by_symbol[obj.symbol].append(obj.id)
            
    def get(self, object_id: str) -> GeometryObject | None:
        return self._cache.get(object_id)
        
    def get_by_type(self, type_name: str, symbol: Optional[str] = None) -> List[GeometryObject]:
        objs = [self._cache[oid] for oid in self._by_type.get(type_name, [])]
        if symbol:
            return [o for o in objs if o.symbol == symbol]
        return objs
        
    def get_by_symbol(self, symbol: str) -> List[GeometryObject]:
        return [self._cache[oid] for oid in self._by_symbol.get(symbol, [])]
        
    def update_last_bar_timestamp(self, timestamp: str) -> None:
        self._last_bar_timestamp = timestamp
        
    def get_last_bar_timestamp(self) -> Optional[str]:
        return self._last_bar_timestamp
        
    def clear(self) -> None:
        self._cache.clear()
        self._by_type.clear()
        self._by_symbol.clear()
        self._last_bar_timestamp = None
