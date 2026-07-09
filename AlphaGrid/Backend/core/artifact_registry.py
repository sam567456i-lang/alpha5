from typing import Dict, Any, Optional
from Backend.core.interfaces.core_interfaces import IArtifactRegistry
import uuid

class ArtifactRegistry(IArtifactRegistry):
    """
    Manages persistent artifacts (Snapshots, Replays, Reports, Models).
    Enforces artifact lineage (DAG) tracking `derived_from`.
    """
    def __init__(self):
        self.artifacts: Dict[str, Dict[str, Any]] = {}
        
    def register_artifact(self, artifact_type: str, data: Any, provenance: Dict[str, Any]) -> str:
        artifact_id = f"art_{uuid.uuid4().hex[:8]}"
        
        # Enforce minimum lineage
        if "derived_from" not in provenance:
            provenance["derived_from"] = None
        if "generated_by" not in provenance:
            provenance["generated_by"] = "system"
            
        self.artifacts[artifact_id] = {
            "type": artifact_type,
            "data": data,
            "provenance": provenance
        }
        return artifact_id
        
    def get_artifact(self, artifact_id: str) -> Optional[Any]:
        return self.artifacts.get(artifact_id)
