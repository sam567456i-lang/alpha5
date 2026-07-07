import os
import yaml
from typing import List, Dict, Any

class RegistryParser:
    """Project OS Registry Parser Engine (Certified for Stage 6)"""
    
    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        self.registry_path = os.path.join(repo_root, "master_capability_registry.yaml")
        self.valid_enums = ["active", "frozen", "deprecated", "experimental", "beta", "production"]
        
    def load_registry(self) -> Dict[str, Any]:
        """Loads the master capability registry deterministically with graceful recovery."""
        if not os.path.exists(self.registry_path):
            print(f"[WARN] Graceful Recovery: Registry missing at {self.registry_path}")
            return {"capabilities": []}
            
        try:
            with open(self.registry_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if not data:
                    return {"capabilities": []}
                return data
        except yaml.YAMLError as e:
            print(f"[ERROR] Corrupt YAML detected: {e}")
            return {"capabilities": []}

    def get_capabilities(self) -> List[Dict[str, Any]]:
        """Extracts capabilities, validating against schema and duplicates."""
        registry = self.load_registry()
        capabilities = []
        seen_ids = set()
        
        for cap in registry.get("capabilities", []):
            if cap.get("entity_type") != "capability":
                continue
                
            cap_id = cap.get("id")
            # 1. Missing Field Validation
            if not cap_id:
                print(f"[ERROR] Capability missing 'id'. Skipping.")
                continue
            if "dto" not in cap:
                print(f"[ERROR] Capability '{cap_id}' missing 'dto'.")
                continue
                
            # 2. Duplicate ID Detection
            if cap_id in seen_ids:
                print(f"[ERROR] Duplicate capability ID detected: {cap_id}")
                continue
            seen_ids.add(cap_id)
            
            # 3. Invalid Enum Validation
            lifecycle = cap.get("lifecycle_status", "").lower()
            if lifecycle and lifecycle not in self.valid_enums and lifecycle != "placeholder":
                print(f"[ERROR] Invalid enum '{lifecycle}' in capability '{cap_id}'")
            
            capabilities.append(cap)
            
        # 4. Stable Output Ordering
        return sorted(capabilities, key=lambda x: x["id"])

    def get_all_entities(self) -> List[Dict[str, Any]]:
        registry = self.load_registry()
        return registry.get("capabilities", [])
