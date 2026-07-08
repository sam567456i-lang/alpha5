from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from Backend.platforms.platform9_concepts.feature_base import BaseFeature
from Backend.shared_domain.contracts.zones.zone_dtos import ZoneDTO

@dataclass(frozen=True)
class ZoneFeature(BaseFeature):
    """
    Platform 9 representation of a Platform 8 Zone.
    Guarantees byte-for-byte immutability of the underlying ZoneDTO.
    """
    zone_dto: Optional[ZoneDTO] = None
    
    def __post_init__(self):
        # Tie the feature ID deterministically to the zone's versioned identity
        if self.zone_dto and not self.feature_id:
            object.__setattr__(self, "feature_id", f"FEAT-{self.zone_dto.identity.zone_id}-v{self.zone_dto.identity.zone_version}")
    
    @property
    def value(self) -> float:
        """Required by BaseFeature, represents the mid-price of the zone."""
        return (self.zone_dto.geometry.upper_price + self.zone_dto.geometry.lower_price) / 2.0
    
    @property
    def timestamp(self) -> datetime:
        return self.zone_dto.created_at
