"""API exception classes and global FastAPI exception handlers."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from .responses import error_response


# ---------------------------------------------------------------------------
# Typed API exceptions
# ---------------------------------------------------------------------------


class APIError(Exception):
    """Base class for all API layer exceptions."""

    status_code: int = 500
    error_code: str = "SYSTEM_ERROR"

    def __init__(self, message: str, details: list | None = None) -> None:  # type: ignore
        super().__init__(message)
        self.message = message
        self.details = details or []


class APIValidationError(APIError):
    """Raised when request input fails validation (400)."""

    status_code = 400
    error_code = "VALIDATION_ERROR"


class APINotFoundError(APIError):
    """Raised when a requested resource does not exist (404)."""

    status_code = 404
    error_code = "NOT_FOUND"


class APIForbiddenError(APIError):
    """Raised when access to a resource is explicitly denied (403)."""

    status_code = 403
    error_code = "FORBIDDEN"


class APIConflictError(APIError):
    """Raised when a create/update operation conflicts with existing state (409)."""

    status_code = 409
    error_code = "CONFLICT"


class APIRateLimitError(APIError):
    """Raised when an API quota or rate limit is exceeded (429)."""

    status_code = 429
    error_code = "RATE_LIMIT"


class APIMarketClosedError(APIError):
    """Raised when a live-market operation is attempted outside market hours (503)."""

    status_code = 503
    error_code = "MARKET_CLOSED"


# ---------------------------------------------------------------------------
# Global FastAPI exception handlers
# ---------------------------------------------------------------------------


def _handle_api_error(request: Request, exc: APIError) -> JSONResponse:
    """Handler for any typed AlphaGrid APIError."""
    return error_response(
        error_code=exc.error_code,
        message=exc.message,
        details=exc.details,
        status_code=exc.status_code,
    )


def _handle_validation_error(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handler for Pydantic request-body validation failures."""
    details = [
        {"loc": list(e["loc"]), "msg": e["msg"]}
        for e in exc.errors()
    ]
    return error_response(
        error_code="VALIDATION_ERROR",
        message="Request validation failed.",
        details=details,
        status_code=400,
    )


def _handle_http_exception(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Handler for Starlette / FastAPI HTTPException."""
    code_map: dict[int, str] = {
        400: "VALIDATION_ERROR",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        409: "CONFLICT",
        429: "RATE_LIMIT",
        503: "MARKET_CLOSED",
    }
    error_code = code_map.get(exc.status_code, "SYSTEM_ERROR")
    return error_response(
        error_code=error_code,
        message=str(exc.detail),
        status_code=exc.status_code,
    )


def _handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler for unhandled exceptions."""
    return error_response(
        error_code="SYSTEM_ERROR",
        message="An unexpected error occurred. Please try again.",
        status_code=500,
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Attach all global exception handlers to the FastAPI application."""
    app.add_exception_handler(APIError, _handle_api_error)  # type: ignore
    app.add_exception_handler(RequestValidationError, _handle_validation_error)  # type: ignore
    app.add_exception_handler(StarletteHTTPException, _handle_http_exception)  # type: ignore
    app.add_exception_handler(Exception, _handle_unexpected_error)

