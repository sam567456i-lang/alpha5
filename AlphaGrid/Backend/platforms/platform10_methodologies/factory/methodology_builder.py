from typing import Dict, Any

class MethodologyBuilder:
    """
    Mutable builder for assembling the pieces of a Methodology assessment.
    """
    def __init__(self, methodology_id: str):
        self._data = {
            "id": methodology_id,
            "name": "",
            "semantic_bias": "Neutral",
            "confidence": 0.0,
            "state": "PENDING_EVALUATION",
            "provenance": None,
            "metadata": {}
        }
        
    def set_name(self, name: str):
        self._data["name"] = name
        return self
        
    def set_bias(self, bias: str):
        self._data["semantic_bias"] = bias
        return self
        
    def set_confidence(self, conf: float):
        self._data["confidence"] = conf
        return self
        
    def set_state(self, state: str):
        self._data["state"] = state
        return self
        
    def set_provenance(self, provenance: Any):
        self._data["provenance"] = provenance
        return self
        
    def build(self) -> Dict[str, Any]:
        # Return a dictionary that will be sent to the factory to freeze
        return self._data
