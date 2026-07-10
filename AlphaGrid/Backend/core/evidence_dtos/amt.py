from dataclasses import dataclass
from Backend.core.evidence_dtos.base import BasePlatformObject

@dataclass
class AuctionStateObject(BasePlatformObject):
    """Root base for Auction Market Theory objects."""
    amt_uuid: str = ""

@dataclass
class Acceptance(AuctionStateObject):
    """Price rotates into an area and builds volume/time."""
    accepted_price_level: float = 0.0
    time_spent_seconds: float = 0.0

@dataclass
class Rejection(AuctionStateObject):
    """Price enters an area and is immediately pushed out."""
    rejected_price_level: float = 0.0
    excess_tail_length: float = 0.0

@dataclass
class FailedAuction(AuctionStateObject):
    """Price attempts to break out of balance, fails, and rotates to the opposite extreme."""
    breakout_level: float = 0.0
    failure_level: float = 0.0

@dataclass
class Balance(AuctionStateObject):
    """Rotational market state. VA overlapping."""
    upper_bound: float = 0.0
    lower_bound: float = 0.0

@dataclass
class ImbalanceState(AuctionStateObject):
    """Directional trending state. VA separating."""
    is_up: bool = True

@dataclass
class InitiativeActivity(AuctionStateObject):
    """Activity driving price away from value."""
    price_level: float = 0.0

@dataclass
class ResponsiveActivity(AuctionStateObject):
    """Activity driving price back toward value."""
    price_level: float = 0.0
