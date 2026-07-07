"""
Facade for legacy DTO imports.
All domain DTOs have been migrated to their respective domain packages:
- Backend.shared_domain.contracts.base.*
- Backend.shared_domain.contracts.liquidity.*
"""

from Backend.shared_domain.contracts.base.lineage import (
    RuntimeTraceDTO,
    SemanticTraceDTO,
    LineageDTO
)

from Backend.shared_domain.contracts.base.confidence import (
    ConfidenceProfileDTO
)

# Export them explicitly
__all__ = [
    "RuntimeTraceDTO",
    "SemanticTraceDTO",
    "LineageDTO",
    "ConfidenceProfileDTO"
]
