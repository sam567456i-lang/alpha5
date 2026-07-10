import hashlib
import json
from typing import Dict, Any, Optional, TypeVar, Generic, List
from enum import Enum

class CRL(Enum):
    CRL0_CONCEPT = 0
    CRL1_ARCHITECTURE = 1
    CRL2_SPECIFICATION = 2
    CRL3_PROTOTYPE = 3
    CRL4_IMPLEMENTED = 4
    CRL5_VERIFIED = 5
    CRL6_PRODUCTION_READY = 6
    CRL7_CERTIFIED = 7
    CRL8_FROZEN = 8
from typing import Dict, Any, Optional, TypeVar, Generic, List

T = TypeVar('T')

class RegistryError(Exception):
    """Exception raised for registry integrity violations."""
    pass

class BaseRegistry(Generic[T]):
    """
    Strict Institutional Base Registry.
    Enforces uniqueness, duplicate detection, versioning, and fingerprinting.
    """
    def __init__(self, registry_name: str, version: str = "1.0.0"):
        self.name = registry_name
        self.version = version
        self._items: Dict[str, T] = {}
        self._fingerprints: Dict[str, str] = {}
        self._crls: Dict[str, CRL] = {}
        self._versions: Dict[str, Dict[str, str]] = {}
        
    def _generate_fingerprint(self, item: Any) -> str:
        """Generates a deterministic fingerprint for an item."""
        # This is a naive implementation; subclasses should override for specific needs.
        if hasattr(item, '__dict__'):
            item_dict = item.__dict__.copy()
            item_dict["__class__"] = item.__class__.__name__
        elif hasattr(item, '_asdict'):
            item_dict = item._asdict()
            item_dict["__class__"] = item.__class__.__name__
        else:
            item_dict = {"value": str(item), "__class__": item.__class__.__name__}
            
        # Sort keys to ensure determinism
        encoded = json.dumps(item_dict, sort_keys=True, default=str).encode('utf-8')
        return hashlib.sha256(encoded).hexdigest()
    def register(self, key: str, item: T, crl: CRL = CRL.CRL0_CONCEPT, versions: Dict[str, str] = None) -> None:
        """
        Registers an item with explicit CRL and version tracking.
        """
        if versions is None:
            versions = {
                "specification": "0.0.0",
                "architecture": "0.0.0",
                "implementation": "0.0.0",
                "certification": "0.0.0"
            }
        if not key:
            raise RegistryError(f"[{self.name}] Registration key cannot be empty.")
            
        if key in self._items:
            raise RegistryError(f"[{self.name}] Duplicate registration detected for key: {key}")
            
        fingerprint = self._generate_fingerprint(item)
        
        # Check for fingerprint collision (exact duplicate object under different key)
        if fingerprint in self._fingerprints.values():
            raise RegistryError(f"[{self.name}] Fingerprint collision detected! Identical item already exists.")
            
        self._items[key] = item
        self._fingerprints[key] = fingerprint
        self._crls[key] = crl
        self._versions[key] = versions

    def get(self, key: str) -> Optional[T]:
        """Retrieves an item by key."""
        return self._items.get(key)
        
    def get_all(self) -> List[T]:
        """Retrieves all registered items."""
        return list(self._items.values())
        
    def verify_integrity(self) -> bool:
        """
        Verifies the integrity of the registry.
        Checks that all items match their recorded fingerprints.
        """
        for key, item in self._items.items():
            expected = self._fingerprints.get(key)
            actual = self._generate_fingerprint(item)
            if expected != actual:
                raise RegistryError(f"[{self.name}] Fingerprint integrity violation for key: {key}. Data was mutated!")
        return True
        
    def export_manifest(self) -> Dict[str, Any]:
        """Exports the registry metadata for audit compliance."""
        return {
            "registry_name": self.name,
            "version": self.version,
            "count": len(self._items),
            "items": list(self._items.keys()),
            "crl_states": {k: v.name for k, v in self._crls.items()},
            "versions": self._versions
        }
