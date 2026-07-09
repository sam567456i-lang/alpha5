from dataclasses import dataclass
from typing import Optional

from Backend.core.analytical_rules.dto.evidence_dto import EvidenceDTO
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO

@dataclass(frozen=True)
class RangePolicy:
    equilibrium_reference: float = 0.5
    premium_boundary: float = 0.5
    discount_boundary: float = 0.5

@dataclass(frozen=True)
class RangeState(EvidenceDTO):
    """
    Tracks price location within established structural topologies (Swing High to Swing Low).
    """
    range_id: str
    upper_bound: float
    lower_bound: float
    policy: RangePolicy
    
    @property
    def range_height(self) -> float:
        return self.upper_bound - self.lower_bound
        
    @property
    def equilibrium(self) -> float:
        return self.lower_bound + (self.range_height * self.policy.equilibrium_reference)
        
    @property
    def premium_threshold(self) -> float:
        return self.lower_bound + (self.range_height * self.policy.premium_boundary)
        
    @property
    def discount_threshold(self) -> float:
        return self.lower_bound + (self.range_height * self.policy.discount_boundary)
