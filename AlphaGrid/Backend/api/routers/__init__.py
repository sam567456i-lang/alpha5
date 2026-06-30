"""Router package exports."""

from .ai import router as ai_router
from .dashboard import router as dashboard_router
from .features import router as features_router
from .market import router as market_router
from .options import router as options_router
from .portfolio import router as portfolio_router
from .recommendations import router as recommendations_router
from .reports import router as reports_router
from .research import router as research_router
from .strategies import router as strategies_router
from .system import router as system_router

__all__ = [
    "ai_router",
    "dashboard_router",
    "features_router",
    "market_router",
    "options_router",
    "portfolio_router",
    "recommendations_router",
    "reports_router",
    "research_router",
    "strategies_router",
    "system_router",
]
