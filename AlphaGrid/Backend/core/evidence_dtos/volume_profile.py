from dataclasses import dataclass
from Backend.core.evidence_dtos.base import BasePlatformObject
from Backend.core.interfaces.profile_framework import ProfileIdentity

# --- Measurements ---
@dataclass
class VolumeHistogramMeasurement:
    """Read-only measurement representing volume-at-price."""
    price_levels: dict # price -> volume sum

# --- Objects (Derived States) ---
@dataclass
class VolumeProfileObject(BasePlatformObject):
    """Root base for Volume Profile concepts."""
    profile_uuid: str = ""

@dataclass
class VolumePOC(VolumeProfileObject):
    price_level: float = 0.0
    total_volume: float = 0.0

@dataclass
class VolumeNode(VolumeProfileObject):
    """Represents HVNs and LVNs."""
    node_type: str = "HVN" # or LVN
    price_level: float = 0.0
    relative_volume: float = 0.0

@dataclass
class VolumeValueArea(VolumeProfileObject):
    vah_price: float = 0.0
    val_price: float = 0.0
    poc_price: float = 0.0
