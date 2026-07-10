import json
import hashlib
from enum import Enum
from typing import Dict, Any, List

class Causality(Enum):
    ONLINE = "ONLINE"    # Strictly causal
    OFFLINE = "OFFLINE"  # Uses future bars (research only)

class MeasurementEngine:
    """
    Base class for all Platform 10 Measurements.
    Owns the mathematics, but NOT the execution loop.
    """
    
    measurement_type = "BaseMeasurement"
    algorithm_id = "BASE_ALGO"
    measurement_schema_version = "1.0.0"
    algorithm_version = "1.0.0"
    causality = Causality.ONLINE
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # Deterministic hashing
        canonical_json = json.dumps(config, sort_keys=True).encode('utf-8')
        self.config_hash = hashlib.sha256(canonical_json).hexdigest()
        self.dataset_id = config.get("dataset_id", "UNKNOWN")
        
    def get_provenance(self) -> Dict[str, str]:
        return {
            "measurement_type": self.measurement_type,
            "algorithm_id": self.algorithm_id,
            "measurement_schema_version": self.measurement_schema_version,
            "algorithm_version": self.algorithm_version,
            "configuration_hash": self.config_hash,
            "dataset_id": self.dataset_id,
            "causality": self.causality.value
        }
        
    def step(self, history: List[Dict[str, Any]], current_idx: int) -> Any:
        """
        Compute the measurement for the current_idx.
        Must be implemented by subclasses.
        """
        raise NotImplementedError
