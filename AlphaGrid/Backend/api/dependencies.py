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


# ---------------------------------------------------------------------------
# Foundation Dependency Injection
# ---------------------------------------------------------------------------

from fastapi import Request, Depends
from Backend.foundation.dependency_injection_container import DependencyContainer
from Backend.api.services.market_service import MarketService
from Backend.market_intelligence.session_engine import SessionEngine
from Backend.market_intelligence.universe_manager import UniverseManager
from Backend.market_intelligence.normalization_engine import NormalizationEngine

def get_container(request: Request) -> DependencyContainer:
    """Retrieve the Foundation DependencyContainer attached to the FastAPI application state."""
    if not hasattr(request.app.state, "container"):
        raise RuntimeError("DependencyContainer is not attached to the FastAPI application state.")
    return request.app.state.container

from Backend.market_intelligence.providers.abstract_market_data_provider import HistoricalDataProvider

def get_market_service(container: DependencyContainer = Depends(get_container)) -> MarketService:
    """Construct MarketService by resolving its domain engine dependencies from the canonical container."""
    session_engine = container.resolve("session_engine", SessionEngine)
    universe_manager = container.resolve("universe_manager", UniverseManager)
    normalization_engine = container.resolve("normalization_engine", NormalizationEngine)
    
    # Resolve the orchestrated pipeline
    from Backend.market_intelligence.historical_market_pipeline import HistoricalMarketPipeline
    pipeline = container.resolve("historical_market_pipeline", HistoricalMarketPipeline)
    
    return MarketService(
        session_engine=session_engine,
        universe_manager=universe_manager,
        normalization_engine=normalization_engine,
        historical_market_pipeline=pipeline,
    )

from Backend.api.services.features_service import FeaturesService
from Backend.api.services.options_service import OptionsService
from Backend.api.services.strategies_service import StrategiesService

def get_features_service(container: DependencyContainer = Depends(get_container)) -> FeaturesService:
    return FeaturesService()

def get_options_service(container: DependencyContainer = Depends(get_container)) -> OptionsService:
    return OptionsService()

def get_strategies_service(container: DependencyContainer = Depends(get_container)) -> StrategiesService:
    return StrategiesService()

from Backend.api.services.recommendations_service import RecommendationsService
from Backend.api.services.portfolio_service import PortfolioService
from Backend.api.services.research_service import ResearchService
from Backend.api.services.ai_service import AIService
from Backend.api.services.reports_service import ReportsService
from Backend.api.services.dashboard_service import DashboardService
from Backend.api.services.system_service import SystemService

def get_recommendations_service(container: DependencyContainer = Depends(get_container)) -> RecommendationsService:
    return RecommendationsService()

def get_portfolio_service(container: DependencyContainer = Depends(get_container)) -> PortfolioService:
    return PortfolioService()

def get_research_service(container: DependencyContainer = Depends(get_container)) -> ResearchService:
    return ResearchService()

def get_ai_service(container: DependencyContainer = Depends(get_container)) -> AIService:
    return AIService()

def get_reports_service(container: DependencyContainer = Depends(get_container)) -> ReportsService:
    return ReportsService()

def get_dashboard_service(container: DependencyContainer = Depends(get_container)) -> DashboardService:
    return DashboardService()

def get_system_service(container: DependencyContainer = Depends(get_container)) -> SystemService:
    return SystemService()
