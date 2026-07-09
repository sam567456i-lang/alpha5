from dataclasses import dataclass
from enum import Enum

class LifecycleState(Enum):
    EXPERIMENTAL = "EXPERIMENTAL"
    STABLE = "STABLE"
    DEPRECATED = "DEPRECATED"
    REMOVED = "REMOVED"

@dataclass(frozen=True)
class ContractVersion:
    """Decoupled versioning for public APIs."""
    api_version: str      # e.g., "1.2" (Interface compatibility)
    schema_version: int   # e.g., 3 (Data structure fields)
    storage_version: int  # e.g., 5 (Persistence format)
    migration_version: int # e.g., 4 (Upgrade mapping path)
    lifecycle_state: LifecycleState = LifecycleState.EXPERIMENTAL
    
class APIVersionManager:
    """Manages API compatibility and lifecycle deprecations."""
    def __init__(self):
        self.contracts = {}
        
    def register_contract(self, name: str, version: ContractVersion):
        self.contracts[name] = version
        
    def check_compatibility(self, name: str, target_api: str) -> bool:
        contract = self.contracts.get(name)
        if not contract:
            return False
        if contract.lifecycle_state == LifecycleState.REMOVED:
            return False
        # Basic check: matching major version
        return contract.api_version.split('.')[0] == target_api.split('.')[0]
