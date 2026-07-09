from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class PoolLifecyclePolicy:
    """
    Policy governing the lifecycle behaviors of pools.
    """
    merge_policy: str = "STRICT_OVERLAP"
    expiration_policy: str = "TIME_DECAY"
    supersede_policy: str = "PRICE_OVERRIDE"
    archive_policy: str = "RETENTION_LIMIT"
