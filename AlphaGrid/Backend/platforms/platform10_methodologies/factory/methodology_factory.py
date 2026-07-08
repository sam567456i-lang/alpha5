import hashlib
from typing import Dict, Any
from Backend.core.interfaces.methodology_dto import MethodologyDTO
from Backend.core.interfaces.methodology_provenance_dto import MethodologyProvenanceDTO

class MethodologyFactory:
    """
    Consumes a mutable builder dictionary, validates it, assigns lineage/fingerprint,
    and returns a strictly immutable, frozen MethodologyDTO.
    """
    def freeze(self, raw_data: Dict[str, Any]) -> MethodologyDTO:
        # Validate required fields
        if not raw_data.get("id"):
            raise ValueError("Methodology must have an ID")
            
        # Assign lineage and fingerprint
        lineage = f"L10_{raw_data['id']}_{hash(str(raw_data.get('provenance')))}"
        fingerprint = hashlib.sha256(str(raw_data).encode()).hexdigest()
        
        # We need to construct a provenance if it's not quite right or patch it
        prov = raw_data.get("provenance")
        if not isinstance(prov, MethodologyProvenanceDTO):
            prov = MethodologyProvenanceDTO(
                lineage=lineage,
                fingerprint=fingerprint
            )
        
        # Instantiate frozen dataclass
        return MethodologyDTO(
            id=raw_data["id"],
            name=raw_data.get("name", ""),
            semantic_bias=raw_data.get("semantic_bias", "Neutral"),
            confidence=raw_data.get("confidence", 0.0),
            state=raw_data.get("state", "FROZEN"),
            provenance=prov,
            metadata=raw_data.get("metadata", {})
        )
