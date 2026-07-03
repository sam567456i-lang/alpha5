import json
import logging
import os

logger = logging.getLogger("RuntimeAuditor.PhaseFreezeValidator")

class PhaseFreezeValidator:
    """Compares diffs of frozen phases against the baseline."""
    
    def __init__(self):
        self.mutations_found = []

    def verify_frozen_phase(self, phase_name: str, baseline_hash: str, current_hash: str):
        if baseline_hash != current_hash:
            self.mutations_found.append({
                "phase": phase_name,
                "expected_hash": baseline_hash,
                "actual_hash": current_hash,
                "status": "MUTATED"
            })

    def export(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "phase_freeze_manifest.json"), "w") as f:
            json.dump({"mutations": self.mutations_found}, f, indent=2)

