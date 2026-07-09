from dataclasses import dataclass

@dataclass(frozen=True)
class SwingIdentityDTO:
    """Immutable identity representing the geometric and policy definition of a swing."""
    id: str
    symbol: str
    timeframe: str
    timestamp: str
    price: float
    direction: str
    policy_id: str
    policy_version: str
    policy_checksum: str
    geometry_fingerprint: str
