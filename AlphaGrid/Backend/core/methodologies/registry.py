from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from Backend.core.methodologies.core_models import MethodologyVersion, MethodologyContext

class MethodologyLifecycle(Enum):
    EXPERIMENTAL = "EXPERIMENTAL"
    RESEARCH = "RESEARCH"
    VALIDATED = "VALIDATED"
    PRODUCTION = "PRODUCTION"
    DEPRECATED = "DEPRECATED"
    RETIRED = "RETIRED"

class Namespace(Enum):
    BUILT_IN = "BUILT_IN"
    INTERNAL_RESEARCH = "INTERNAL_RESEARCH"
    EXTERNAL_PLUGIN = "EXTERNAL_PLUGIN"

@dataclass(frozen=True)
class MethodologyManifest:
    """Machine-readable metadata for a methodology version."""
    version_ref: MethodologyVersion
    namespace: Namespace
    lifecycle: MethodologyLifecycle
    requires_families: List[str] = field(default_factory=list)
    requires_objects: List[str] = field(default_factory=list)
    optional_families: List[str] = field(default_factory=list)
    supported_assets: List[str] = field(default_factory=list)
    supported_timeframes: List[str] = field(default_factory=list)
    supported_regimes: List[str] = field(default_factory=list)

class MethodologyRegistry:
    """Dynamic catalog for built-in, internal, and external plugin methodologies."""
    def __init__(self):
        self._manifests: Dict[str, MethodologyManifest] = {}

    def register(self, manifest: MethodologyManifest):
        key = f"{manifest.version_ref.definition.methodology_id}.{manifest.version_ref.version_id}"
        self._manifests[key] = manifest
        
    def get_manifest(self, methodology_id: str, version_id: str) -> MethodologyManifest:
        key = f"{methodology_id}.{version_id}"
        if key not in self._manifests:
            raise KeyError(f"Unregistered methodology: {key}")
        return self._manifests[key]

class CapabilityNegotiation:
    """Negotiates methodology capabilities against an incoming context snapshot."""
    @staticmethod
    def negotiate(manifest: MethodologyManifest, context: MethodologyContext) -> str:
        # Check requirements against context available_capabilities
        for req in manifest.requires_families:
            if req not in context.available_capabilities:
                return "UNSUPPORTED"
        return "FULL"
