from typing import Type
import inspect
import os
import yaml
from Backend.platforms.platform8_analysis.frameworks.detector_base import DetectorBase
from Backend.core.state import ExecutionContext, StateLifecycle
from datetime import datetime

class DetectorCertificationSuite:
    """
    Gate 3 Certification Suite.
    Validates any custom DetectorBase subclass to ensure it conforms to
    the rigid structural rules of Platform 8 Analysis Framework.
    """
    
    @staticmethod
    def certify(detector_class: Type[DetectorBase], capability_id: str, repo_root: str) -> bool:
        print(f"Starting certification for {detector_class.__name__} (Capability: {capability_id})...")
        
        # 1. Must inherit from DetectorBase
        if not issubclass(detector_class, DetectorBase):
            print(f"FAIL: {detector_class.__name__} does not inherit from DetectorBase.")
            return False
            
        # 2. Behavior Registry Validation
        behavior_reg_path = os.path.join(repo_root, "Docs", "Governance", "registry", "behavior_registry.yaml")
        cap_reg_path = os.path.join(repo_root, "Docs", "Governance", "registry", "capability_registry.yaml")
        
        if os.path.exists(behavior_reg_path) and os.path.exists(cap_reg_path):
            with open(cap_reg_path, "r", encoding="utf-8") as f:
                all_caps = {c["id"] for c in (yaml.safe_load(f) or {}).get("entries", [])}
                
            with open(behavior_reg_path, "r", encoding="utf-8") as f:
                behaviors = (yaml.safe_load(f) or {}).get("entries", [])
                
            for b in behaviors:
                if b["subject_id"] == capability_id:
                    for s in b.get("supports", []):
                        if s not in all_caps:
                            print(f"FAIL: Behavior Registry semantic reference invalid. {capability_id} supports {s} but {s} doesn't exist.")
                            return False
                    for i in b.get("invalidates", []):
                        if i not in all_caps:
                            print(f"FAIL: Behavior Registry semantic reference invalid. {capability_id} invalidates {i} but {i} doesn't exist.")
                            return False
                            
        print(f"PASS: {detector_class.__name__} successfully certified.")
        return True
