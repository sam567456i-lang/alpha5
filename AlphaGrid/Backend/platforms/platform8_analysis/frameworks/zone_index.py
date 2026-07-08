from abc import ABC, abstractmethod
from typing import List, Optional
from Backend.shared_domain.contracts.zones.zone_dtos import ZoneDTO

class ZoneIndex(ABC):
    """
    Spatial Index Abstraction.
    Allows downstream implementations like IntervalTreeIndex, RTreeIndex, or KDTreeIndex
    to be substituted without affecting the detectors.
    """
    @abstractmethod
    def insert(self, zone: ZoneDTO) -> None: pass
    
    @abstractmethod
    def remove(self, zone_id: str) -> None: pass
    
    @abstractmethod
    def get_zone(self, zone_id: str) -> Optional[ZoneDTO]: pass
    
    @abstractmethod
    def find_overlapping(self, upper_price: float, lower_price: float) -> List[ZoneDTO]: pass
    
    @abstractmethod
    def find_containing(self, upper_price: float, lower_price: float) -> List[ZoneDTO]: pass
    
    @abstractmethod
    def find_nearest(self, price: float, limit: int = 1) -> List[ZoneDTO]: pass
    
    @abstractmethod
    def find_by_price(self, price: float) -> List[ZoneDTO]: pass
    
    @abstractmethod
    def find_by_time(self, start_timestamp, end_timestamp=None) -> List[ZoneDTO]: pass
    
    @abstractmethod
    def find_active(self) -> List[ZoneDTO]: pass
    
    @abstractmethod
    def find_invalidated(self) -> List[ZoneDTO]: pass
    
    @abstractmethod
    def clear(self) -> None: pass
    
    @abstractmethod
    def __len__(self) -> int: pass

class ListZoneIndex(ZoneIndex):
    """Concrete implementation using a flat list."""
    def __init__(self):
        self._zones: List[ZoneDTO] = []
        
    def insert(self, zone: ZoneDTO) -> None:
        self._zones.append(zone)
        
    def remove(self, zone_id: str) -> None:
        self._zones = [z for z in self._zones if z.identity.zone_id != zone_id]
        
    def get_zone(self, zone_id: str) -> Optional[ZoneDTO]:
        for z in self._zones:
            if z.identity.zone_id == zone_id:
                return z
        return None
        
    def find_overlapping(self, upper_price: float, lower_price: float) -> List[ZoneDTO]:
        results = []
        for z in self._zones:
            if max(lower_price, z.geometry.lower_price) <= min(upper_price, z.geometry.upper_price):
                results.append(z)
        return results

    def find_containing(self, upper_price: float, lower_price: float) -> List[ZoneDTO]:
        return [z for z in self._zones if z.geometry.upper_price >= upper_price and z.geometry.lower_price <= lower_price]

    def find_nearest(self, price: float, limit: int = 1) -> List[ZoneDTO]:
        # Naive distance logic
        sorted_zones = sorted(self._zones, key=lambda z: min(abs(z.geometry.upper_price - price), abs(z.geometry.lower_price - price)))
        return sorted_zones[:limit]

    def find_by_price(self, price: float) -> List[ZoneDTO]:
        return [z for z in self._zones if z.geometry.lower_price <= price <= z.geometry.upper_price]

    def find_by_time(self, start_timestamp, end_timestamp=None) -> List[ZoneDTO]:
        # Naive overlap logic
        return [z for z in self._zones if z.start_timestamp >= start_timestamp]

    def find_active(self) -> List[ZoneDTO]:
        return [z for z in self._zones if z.status.value == "ACTIVE"]

    def find_invalidated(self) -> List[ZoneDTO]:
        return [z for z in self._zones if z.status.value == "INVALIDATED"]

    def clear(self) -> None:
        self._zones.clear()

    def __len__(self) -> int:
        return len(self._zones)
