from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from Backend.core.data_foundation.contracts.schemas import DatasetManifest

class CatalogException(Exception):
    pass

class CatalogQuery:
    def __init__(self):
        self.symbol: Optional[str] = None
        self.resolution: Optional[str] = None
        self.market: Optional[str] = None
        self.provider: Optional[str] = None
        self.dataset_id: Optional[str] = None
        self.hash: Optional[str] = None
        self.asset_type: Optional[str] = None
        self.date_start: Optional[str] = None
        self.date_end: Optional[str] = None

class CatalogBackend(ABC):
    """Abstract interface for storing and querying the Dataset Catalog."""
    
    @abstractmethod
    def register_dataset(self, manifest: DatasetManifest):
        pass
        
    @abstractmethod
    def get_dataset(self, dataset_hash: str) -> Optional[DatasetManifest]:
        pass
        
    @abstractmethod
    def search(self, query: CatalogQuery) -> List[DatasetManifest]:
        pass
        
    @abstractmethod
    def list_all(self) -> List[DatasetManifest]:
        pass

class MemoryCatalog(CatalogBackend):
    """In-memory implementation of CatalogBackend with manual indexing."""
    
    def __init__(self):
        self._manifests: Dict[str, DatasetManifest] = {}
        # Indexes
        self._idx_symbol: Dict[str, set] = {}
        self._idx_resolution: Dict[str, set] = {}
        self._idx_market: Dict[str, set] = {}
        self._idx_provider: Dict[str, set] = {}
        
    def _update_index(self, index: Dict[str, set], key: str, value: str):
        if not key: return
        if key not in index:
            index[key] = set()
        index[key].add(value)
        
    def register_dataset(self, manifest: DatasetManifest):
        h = manifest.dataset_hash
        if h in self._manifests:
            raise CatalogException(f"Dataset {h} already registered.")
            
        self._manifests[h] = manifest
        
        # In a real DB, these would be indexed columns. 
        # Since we use Memory, we build python dict indexes.
        # Wait, the manifest tracks symbol/asset for discovery.
        self._update_index(self._idx_symbol, manifest.symbol, h)
        self._update_index(self._idx_provider, manifest.provider, h)
        self._update_index(self._idx_market, manifest.market, h)
        self._update_index(self._idx_resolution, manifest.resolution, h)
        
    def get_dataset(self, dataset_hash: str) -> Optional[DatasetManifest]:
        return self._manifests.get(dataset_hash)
        
    def search(self, query: CatalogQuery) -> List[DatasetManifest]:
        # Intersect indexes
        candidates = set(self._manifests.keys())
        
        if query.hash and query.hash in candidates:
            candidates = {query.hash}
            
        if query.symbol and query.symbol in self._idx_symbol:
            candidates = candidates.intersection(self._idx_symbol[query.symbol])
            
        if query.provider and query.provider in self._idx_provider:
            candidates = candidates.intersection(self._idx_provider[query.provider])
            
        if query.market and query.market in self._idx_market:
            candidates = candidates.intersection(self._idx_market[query.market])
            
        if query.resolution and query.resolution in self._idx_resolution:
            candidates = candidates.intersection(self._idx_resolution[query.resolution])
            
        return [self._manifests[c] for c in candidates]
        
    def list_all(self) -> List[DatasetManifest]:
        return list(self._manifests.values())

class DatasetCatalog:
    """The central registry for all datasets. Acts as a facade over CatalogBackend."""
    
    def __init__(self, backend: CatalogBackend):
        self.backend = backend
        
    def register(self, manifest: DatasetManifest):
        self.backend.register_dataset(manifest)
        
    def resolve(self, dataset_hash: str) -> Optional[DatasetManifest]:
        return self.backend.get_dataset(dataset_hash)
        
    def discover(self, query: CatalogQuery) -> List[DatasetManifest]:
        return self.backend.search(query)
