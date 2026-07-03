import json
import logging
import os
from typing import Dict, Any

logger = logging.getLogger("RuntimeAuditor.E2EFingerprintProof")

class FingerprintTracer:
    """Explicitly tracks fingerprint propagation across the entire pipeline."""
    
    def __init__(self):
        self.propagation_chain = []

    def log_stage(self, stage: str, object_id: str, fingerprint: str, parent_fingerprint: str = None):
        self.propagation_chain.append({
            "stage": stage,
            "object_id": object_id,
            "fingerprint": fingerprint,
            "parent_fingerprint": parent_fingerprint
        })
        logger.info(f"Fingerprint propagated at {stage}: {fingerprint}")

    def export(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "fingerprint_propagation.json"), "w") as f:
            json.dump({"chain": self.propagation_chain}, f, indent=2)

