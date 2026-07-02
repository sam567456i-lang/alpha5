"""FastAPI middleware: request timing and structured request logging."""

from __future__ import annotations

import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from Backend.foundation.logger import get_logger

_logger = get_logger("alphagrid.api.middleware")


class RequestTimingMiddleware(BaseHTTPMiddleware):
    """Measures wall-clock processing time and injects it into response headers.

    Downstream response helpers read ``request.state.execution_time`` so the
    timing is also available inside route handlers without re-measuring.
    """

    async def dispatch(self, request: Request, call_next: Any) -> Response:

        start = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - start
        request.state.execution_time = elapsed
        response.headers["X-Execution-Time"] = f"{elapsed:.4f}s"
        return response  # type: ignore


class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    """Emits one structured log line per HTTP request."""

    async def dispatch(self, request: Request, call_next: Any) -> Response:

        response = await call_next(request)
        _logger.info(
            "%s %s → %s",
            request.method,
            request.url.path,
            response.status_code,
        )
        return response  # type: ignore


# typing alias used inside the class bodies
from typing import Any  # noqa: E402  (import after class definitions is intentional)
