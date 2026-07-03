from typing import Dict, List, Optional
from Backend.price_geometry.objects import GeometryObject
from Backend.foundation.base_registry import RegistryError

class GeometryStore:
    """
    Centralized store and cache for all computed geometry objects.
    Prevents recomputing geometry on every replay.
    """
    
    def __init__(self):
        self._objects: Dict[str, GeometryObject] = {}
        self._by_dataset: Dict[str, List[str]] = {}
        
    def save(self, obj: GeometryObject) -> None:
        """Stores an immutable geometry object."""
        if obj.id in self._objects:
            # Check for conflict
            existing = self._objects[obj.id]
            if existing.fingerprint != obj.fingerprint:
                raise RegistryError(f"Fingerprint mismatch for Geometry ID {obj.id}")
            return # Already cached
            
        self._objects[obj.id] = obj
        
        if obj.dataset_id not in self._by_dataset:
            self._by_dataset[obj.dataset_id] = []
        self._by_dataset[obj.dataset_id].append(obj.id)
        
    def get(self, obj_id: str) -> Optional[GeometryObject]:
        """Retrieves a geometry object by ID."""
        return self._objects.get(obj_id)
        
    def get_by_dataset(self, dataset_id: str) -> List[GeometryObject]:
        """Retrieves all geometry objects for a dataset."""
        ids = self._by_dataset.get(dataset_id, [])
        return [self._objects[oid] for oid in ids]
        
    def clear(self) -> None:
        """Clears the store (e.g. for testing)."""
        self._objects.clear()
        self._by_dataset.clear()
