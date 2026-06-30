"""FastAPI dependency-injection helpers for the AlphaGrid API layer."""

from __future__ import annotations

from dataclasses import dataclass

from fastapi import Query


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class PaginationParams:
    """Common pagination query parameters injected into list endpoints."""

    page: int
    page_size: int


def get_pagination(
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)."),
    page_size: int = Query(
        default=50, ge=1, le=500, description="Results per page."
    ),
) -> PaginationParams:
    """FastAPI dependency: extract and validate pagination query parameters."""
    return PaginationParams(page=page, page_size=page_size)
