import hashlib
import json
from typing import Dict, Any

class EventReplayValidator:
    def __init__(self):
        self.live_hashes: Dict[str, str] = {}
        self.total_validated = 0
        self.mismatches_found = 0

    def _hash_state(self, state_dict: Dict[str, Any]) -> str:
        state_json = json.dumps(state_dict, sort_keys=True)
        return hashlib.sha256(state_json.encode('utf-8')).hexdigest()

    def record_live_state(self, timestamp: str, capability_id: str, state_dict: Dict[str, Any]):
        key = f"{capability_id}_{timestamp}"
        self.live_hashes[key] = self._hash_state(state_dict)

    def validate_replay_state(self, timestamp: str, capability_id: str, state_dict: Dict[str, Any]) -> bool:
        key = f"{capability_id}_{timestamp}"
        expected_hash = self.live_hashes.get(key)
        actual_hash = self._hash_state(state_dict)

        self.total_validated += 1
        if expected_hash != actual_hash:
            self.mismatches_found += 1
            return False
        return True

    def get_validation_report(self) -> Dict[str, Any]:
        return {
            "is_deterministic": self.mismatches_found == 0,
            "total_validated": self.total_validated,
            "mismatches_found": self.mismatches_found
        }
