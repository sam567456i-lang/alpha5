import os
import yaml
from typing import List, Dict, Any
from ProjectOS.registry.parser import RegistryParser

class SwitchGenerator:
    """Project OS Stage 9: Universal Switch Engine"""
    
    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        self.parser = RegistryParser(repo_root)
        self.output_path = os.path.join(repo_root, "Docs", "Governance", "universal_switches.yaml")
        
    def generate_registry(self):
        print("Generating Universal Switch Registry...")
        capabilities = self.parser.get_capabilities()
        
        switches = {
            "version": "1.0",
            "scopes": {
                "platforms": {},
                "capabilities": {}
            }
        }
        
        for cap in capabilities:
            cap_id = cap.get("id")
            if not cap_id: continue
            
            # Default mapping from capability lifecycle to switch lifecycle
            lifecycle = cap.get("lifecycle_status", "experimental").lower()
            if lifecycle == "placeholder":
                state = "disabled"
            else:
                state = "enabled"
                
            switches["scopes"]["capabilities"][cap_id] = {
                "state": state,
                "lifecycle": lifecycle
            }
            
            # Map platforms dynamically
            platform = cap.get("platform")
            if platform and platform not in switches["scopes"]["platforms"]:
                switches["scopes"]["platforms"][platform] = {
                    "state": "enabled",
                    "lifecycle": "beta"
                }
                
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, "w", encoding="utf-8") as f:
            yaml.dump(switches, f, sort_keys=True, default_flow_style=False)
            
        print(f"Universal Switch Registry generated at {self.output_path}")

if __name__ == "__main__":
    repo_root = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
    gen = SwitchGenerator(repo_root)
    gen.generate_registry()
