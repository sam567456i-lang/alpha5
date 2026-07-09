from dataclasses import dataclass
from typing import Dict, Optional, TypeVar, Type, Any

class RegionExtensionPayload:
    """Base class for strongly-typed region metadata extensions."""
    pass

@dataclass(frozen=True)
class OrderBlockMetadata(RegionExtensionPayload):
    initiating_volume: Optional[float] = None
    time_in_consolidation: Optional[int] = None

@dataclass(frozen=True)
class FVGMetadata(RegionExtensionPayload):
    displacement_velocity: Optional[float] = None

@dataclass(frozen=True)
class RegionMetadataDTO:
    """
    Extensible metadata container for RegionState.
    Uses typed payloads instead of an untyped generic dictionary.
    """
    extensions: Dict[str, RegionExtensionPayload] = None
    
    def __post_init__(self):
        if self.extensions is None:
            # We use object.__setattr__ because the class is frozen
            object.__setattr__(self, 'extensions', {})
            
    def get_extension(self, extension_type: str) -> Optional[RegionExtensionPayload]:
        return self.extensions.get(extension_type)
        
    def with_extension(self, extension_type: str, payload: RegionExtensionPayload) -> 'RegionMetadataDTO':
        new_exts = dict(self.extensions)
        new_exts[extension_type] = payload
        return RegionMetadataDTO(extensions=new_exts)
