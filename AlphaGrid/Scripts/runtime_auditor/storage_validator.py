import json
import logging
import os

logger = logging.getLogger("RuntimeAuditor.StorageValidator")

class StorageValidator:
    """Validates Store to Persistence lifecycle consistency."""
    
    def __init__(self):
        self.store_checks = {}

    def audit_store(self, store_name: str, has_versioning: bool, has_fingerprinting: bool):
        self.store_checks[store_name] = {
            "versioned": has_versioning,
            "fingerprinted": has_fingerprinting,
            "status": "PASS" if has_versioning and has_fingerprinting else "FAIL"
        }

    def export(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "storage_consistency.json"), "w") as f:
            json.dump(self.store_checks, f, indent=2)

