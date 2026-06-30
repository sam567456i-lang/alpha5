"""Standard response envelope helpers for the AlphaGrid API layer."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi.responses import JSONResponse


def _now_iso() -> str:
    """Return the current UTC timestamp as an ISO-8601 string."""
    return datetime.now(tz=timezone.utc).isoformat()


def success_response(
    data: Any = None,
    message: str = "OK",
    execution_time: float = 0.0,
    status_code: int = 200,
) -> JSONResponse:
    """Return a standard success envelope."""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data,
            "timestamp": _now_iso(),
            "execution_time": round(execution_time, 4),
        },
    )


def created_response(
    data: Any = None,
    message: str = "Created",
    execution_time: float = 0.0,
) -> JSONResponse:
    """Return a standard 201 Created envelope."""
    return success_response(
        data=data,
        message=message,
        execution_time=execution_time,
        status_code=201,
    )


def no_content_response() -> JSONResponse:
    """Return a 204 No Content response."""
    return JSONResponse(status_code=204, content=None)


def error_response(
    error_code: str,
    message: str,
    details: list[Any] | None = None,
    status_code: int = 400,
) -> JSONResponse:
    """Return a standard error envelope."""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error_code": error_code,
            "message": message,
            "details": details or [],
            "timestamp": _now_iso(),
        },
    )


def paginated_response(
    data: list[Any],
    total: int,
    page: int,
    page_size: int,
    message: str = "OK",
    execution_time: float = 0.0,
) -> JSONResponse:
    """Return a paginated list envelope."""
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": message,
            "data": data,
            "pagination": {
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": max(1, (total + page_size - 1) // page_size),
            },
            "timestamp": _now_iso(),
            "execution_time": round(execution_time, 4),
        },
    )
