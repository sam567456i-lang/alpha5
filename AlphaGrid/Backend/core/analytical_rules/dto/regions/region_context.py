from dataclasses import dataclass
from typing import List
from Backend.core.analytical_rules.dto.liquidity.price_observation import PriceObservationDTO
from Backend.core.analytical_rules.dto.regions.region_geometry import RegionGeometryDTO
from Backend.core.analytical_rules.dto.regions.region_identity import RegionIdentityDTO
from Backend.core.analytical_rules.dto.regions.region_events import RegionReferenceType

@dataclass(frozen=True)
class RegionInteractionContextDTO:
    """
    Standardized context payload containing the region, observation, and policy parameters.
    Allows interaction rules to be extensible without breaking API signatures.
    """
    region_identity: RegionIdentityDTO
    region_geometry: RegionGeometryDTO
    observation: PriceObservationDTO
    target_references: List[RegionReferenceType]  # E.g. [CENTER, 25_PERCENT]
    policy_overrides: dict  # Optional policy flags (e.g. require_body_close=True)
