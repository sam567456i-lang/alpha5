"""AlphaGrid FastAPI application factory."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Any

from Backend.api.exceptions import register_exception_handlers
from Backend.api.middleware import RequestTimingMiddleware, StructuredLoggingMiddleware
from Backend.api.routers import (
    ai_router,
    dashboard_router,
    features_router,
    market_router,
    options_router,
    portfolio_router,
    recommendations_router,
    reports_router,
    research_router,
    strategies_router,
    system_router,
)
from Backend.api.websocket import websocket_router

_API_PREFIX = "/api/v1"

_DEFAULT_CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]


def create_app(
    container: Any = None,
    title: str = "AlphaGrid Infinity X 5.0",
    version: str = "5.0.0",
    debug: bool = False,
    cors_origins: list[str] | None = None,
) -> FastAPI:
    """Create and configure the AlphaGrid FastAPI application.

    This factory is the single entry point for the entire API layer. It:
    - Registers all 11 domain routers under /api/v1/
    - Registers the 6 WebSocket channels under /ws/
    - Attaches middleware (CORS, timing, logging)
    - Registers global exception handlers
    """
    app = FastAPI(
        title=title,
        version=version,
        debug=debug,
        description=(
            "AlphaGrid Infinity X 5.0 — Institutional-grade quantitative research, "
            "options analytics, portfolio intelligence, and execution platform."
        ),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    if container is None:
        from Backend.foundation.application_entrypoint import create_application_context

        application_context = create_application_context()
        app.state.application_context = application_context
        app.state.container = application_context.container
    else:
        app.state.container = container

    # ------------------------------------------------------------------
    # Middleware (outermost first)
    # ------------------------------------------------------------------
    allowed_origins = cors_origins or _DEFAULT_CORS_ORIGINS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestTimingMiddleware)
    app.add_middleware(StructuredLoggingMiddleware)

    # ------------------------------------------------------------------
    # Exception handlers
    # ------------------------------------------------------------------
    register_exception_handlers(app)

    # ------------------------------------------------------------------
    # REST routers — all mounted under /api/v1
    # ------------------------------------------------------------------
    for router in [
        market_router,
        options_router,
        features_router,
        strategies_router,
        recommendations_router,
        portfolio_router,
        research_router,
        ai_router,
        reports_router,
        dashboard_router,
        system_router,
    ]:
        app.include_router(router, prefix=_API_PREFIX)

    # ------------------------------------------------------------------
    # WebSocket channels — mounted at root (no /api/v1 prefix)
    # ------------------------------------------------------------------
    app.include_router(websocket_router)

    return app
