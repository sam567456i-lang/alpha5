from dataclasses import dataclass, field
from typing import List
from enum import Enum

class PoolSide(Enum):
    BUY_SIDE = "BUY_SIDE"
    SELL_SIDE = "SELL_SIDE"

@dataclass(frozen=True)
class PoolIdentityDTO:
    """
    Immutable identity mapping for a liquidity pool.
    """
    pool_id: str
    pool_side: PoolSide
    anchor_ids: List[str]
    graph_namespace: str
    policy_checksum: str
    geometry_fingerprint: str
