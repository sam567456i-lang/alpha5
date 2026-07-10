from abc import ABC, abstractmethod
from typing import Any, List, Dict, Iterator
import os
from Backend.core.data_foundation.contracts.schemas import DatasetManifest

class StorageException(Exception):
    pass

class PartitionIterator(ABC):
    """Abstract iterator for consuming partitions deterministically."""
    @abstractmethod
    def __iter__(self) -> Iterator[List[Any]]:
        pass
    
    @abstractmethod
    def __next__(self) -> List[Any]:
        pass

class StorageBackend(ABC):
    """Synchronous interface for all underlying storage engines."""
    
    @abstractmethod
    def read_dataset(self, manifest: DatasetManifest) -> PartitionIterator:
        """Returns a PartitionIterator that hides physical layout from consumers."""
        pass
        
    @abstractmethod
    def write_dataset(self, dataset_hash: str, stream: List[Any]) -> int:
        """Consumes a stream of data and autonomously partitions it. Returns partition count."""
        pass
        
    @abstractmethod
    def write_partition(self, canonical_path: str, data: List[Any]):
        """Writes data to the specified canonical path."""
        pass
        
    @abstractmethod
    def read_partition(self, canonical_path: str) -> List[Any]:
        """Reads data from the specified canonical path."""
        pass
        
    @abstractmethod
    def exists(self, canonical_path: str) -> bool:
        """Checks if a partition exists."""
        pass
        
    @abstractmethod
    def delete_partition(self, canonical_path: str):
        """Deletes a partition."""
        pass
        
    @abstractmethod
    def list_partitions(self, base_path: str) -> List[str]:
        """Lists all partitions under a base path."""
        pass
        
    @abstractmethod
    def metadata(self, canonical_path: str) -> Dict[str, Any]:
        """Returns metadata about the partition (size, rows, etc)."""
        pass
        
    @abstractmethod
    def vacuum(self):
        """Reclaims space."""
        pass
        
    @abstractmethod
    def compact(self, base_path: str):
        """Compacts many small partitions into fewer large ones."""
        pass

class StorageRegistry:
    """Dependency Injection registry for storage backends."""
    def __init__(self):
        self._backends: Dict[str, StorageBackend] = {}
        
    def register(self, backend_id: str, backend: StorageBackend):
        if backend_id in self._backends:
            raise StorageException(f"Storage backend {backend_id} already registered.")
        self._backends[backend_id] = backend
        
    def get(self, backend_id: str) -> StorageBackend:
        if backend_id not in self._backends:
            raise StorageException(f"Storage backend {backend_id} not found.")
        return self._backends[backend_id]

# Placeholder Implementations

class ParquetBackend(StorageBackend):
    def read_dataset(self, manifest: DatasetManifest) -> PartitionIterator: raise NotImplementedError
    def write_dataset(self, dataset_hash: str, stream: List[Any]) -> int: raise NotImplementedError
    def write_partition(self, canonical_path: str, data: List[Any]): raise NotImplementedError
    def read_partition(self, canonical_path: str) -> List[Any]: raise NotImplementedError
    def exists(self, canonical_path: str) -> bool: raise NotImplementedError
    def delete_partition(self, canonical_path: str): raise NotImplementedError
    def list_partitions(self, base_path: str) -> List[str]: raise NotImplementedError
    def metadata(self, canonical_path: str) -> Dict[str, Any]: raise NotImplementedError
    def vacuum(self): raise NotImplementedError
    def compact(self, base_path: str): raise NotImplementedError

class DuckDBBackend(StorageBackend):
    def read_dataset(self, manifest: DatasetManifest) -> PartitionIterator: raise NotImplementedError
    def write_dataset(self, dataset_hash: str, stream: List[Any]) -> int: raise NotImplementedError
    def write_partition(self, canonical_path: str, data: List[Any]): raise NotImplementedError
    def read_partition(self, canonical_path: str) -> List[Any]: raise NotImplementedError
    def exists(self, canonical_path: str) -> bool: raise NotImplementedError
    def delete_partition(self, canonical_path: str): raise NotImplementedError
    def list_partitions(self, base_path: str) -> List[str]: raise NotImplementedError
    def metadata(self, canonical_path: str) -> Dict[str, Any]: raise NotImplementedError
    def vacuum(self): raise NotImplementedError
    def compact(self, base_path: str): raise NotImplementedError

class MemoryPartitionIterator(PartitionIterator):
    def __init__(self, data: List[List[Any]]):
        self._data = data
        self._idx = 0
        
    def __iter__(self):
        return self
        
    def __next__(self) -> List[Any]:
        if self._idx >= len(self._data):
            raise StopIteration
        val = self._data[self._idx]
        self._idx += 1
        return val

class MemoryBackend(StorageBackend):
    """In-memory backend for fast tests."""
    def __init__(self):
        self._store: Dict[str, List[Any]] = {}
        
    def read_dataset(self, manifest: DatasetManifest) -> PartitionIterator:
        # Simplistic assumption for tests: just yield whatever matches dataset_id
        matching = [v for k, v in self._store.items() if manifest.dataset_hash in k]
        return MemoryPartitionIterator(matching)
        
    def write_dataset(self, dataset_hash: str, stream: List[Any]) -> int:
        self._store[f"{dataset_hash}_part_0"] = stream
        return 1
        
    def write_partition(self, canonical_path: str, data: List[Any]):
        self._store[canonical_path] = data
        
    def read_partition(self, canonical_path: str) -> List[Any]:
        if canonical_path not in self._store:
            raise StorageException(f"Partition {canonical_path} not found.")
        return self._store[canonical_path]
        
    def exists(self, canonical_path: str) -> bool:
        return canonical_path in self._store
        
    def delete_partition(self, canonical_path: str):
        if canonical_path in self._store:
            del self._store[canonical_path]
            
    def list_partitions(self, base_path: str) -> List[str]:
        return [k for k in self._store.keys() if k.startswith(base_path)]
        
    def metadata(self, canonical_path: str) -> Dict[str, Any]:
        if canonical_path not in self._store:
            raise StorageException(f"Partition {canonical_path} not found.")
        return {"row_count": len(self._store[canonical_path])}
        
    def vacuum(self):
        pass
        
    def compact(self, base_path: str):
        pass

class SQLiteBackend(StorageBackend):
    def read_dataset(self, manifest: DatasetManifest) -> PartitionIterator: raise NotImplementedError
    def write_dataset(self, dataset_hash: str, stream: List[Any]) -> int: raise NotImplementedError
    def write_partition(self, canonical_path: str, data: List[Any]): raise NotImplementedError
    def read_partition(self, canonical_path: str) -> List[Any]: raise NotImplementedError
    def exists(self, canonical_path: str) -> bool: raise NotImplementedError
    def delete_partition(self, canonical_path: str): raise NotImplementedError
    def list_partitions(self, base_path: str) -> List[str]: raise NotImplementedError
    def metadata(self, canonical_path: str) -> Dict[str, Any]: raise NotImplementedError
    def vacuum(self): raise NotImplementedError
    def compact(self, base_path: str): raise NotImplementedError
