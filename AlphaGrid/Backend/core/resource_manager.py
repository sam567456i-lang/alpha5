from Backend.core.interfaces.core_interfaces import IResourceManager
from typing import Dict, Any

class ResourceManager(IResourceManager):
    def __init__(self):
        self.allocations: Dict[str, Dict[str, Any]] = {}
        
    def allocate(self, component: str, memory_mb: int, cpu_shares: int) -> bool:
        # Stub logic to enforce budgets
        self.allocations[component] = {"memory": memory_mb, "cpu": cpu_shares}
        return True
        
    def release(self, component: str):
        if component in self.allocations:
            del self.allocations[component]
