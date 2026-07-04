import yaml
import os
from Backend.platforms.analysis.contracts import AnalysisMetadata

class RegistryLoader:
    def __init__(self, registry_path: str):
        self.registry_path = registry_path
        self._cache = {}
        self.load()
        
    def load(self):
        if not os.path.exists(self.registry_path):
            raise FileNotFoundError(f"Registry not found: {self.registry_path}")
        with open(self.registry_path, "r") as f:
            data = yaml.safe_load(f)
            
        for cap in data.get("capabilities", []):
            cid = cap.get("capability_id")
            if cid:
                self._cache[cid] = AnalysisMetadata(
                    capability_id=cid,
                    platform=cap.get("platform", "P05"),
                    family=cap.get("family", "Unknown"),
                    subfamily=cap.get("subfamily", "Unknown"),
                    dependencies=cap.get("dependencies", [])
                )
                
    def get_metadata(self, capability_id: str) -> AnalysisMetadata:
        if capability_id not in self._cache:
            raise ValueError(f"Capability {capability_id} not found in registry.")
        return self._cache[capability_id]
