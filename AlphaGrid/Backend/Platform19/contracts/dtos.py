from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

# --- INPUT (Queries from Frontend) ---

@dataclass(frozen=True)
class SemanticFilterDTO:
    confidence_min: float
    freshness_required: List[str]
    methodologies: List[str]
    markets: List[str]

@dataclass(frozen=True)
class PresentationQueryDTO:
    semantic_filters: SemanticFilterDTO
    sort_by: str
    sort_order: str
    page: int
    page_size: int
    active_workspace_id: str
    active_layout_id: str

# --- OUTPUT (View Models to Frontend) ---

@dataclass(frozen=True)
class ScannerViewDTO:
    opportunity_id: str
    symbol: str
    confidence_display: str
    freshness_display: str
    primary_evidence: str
    risk_level: str

@dataclass(frozen=True)
class WatchlistDTO:
    watchlist_id: str
    name: str
    symbols: List[str]

@dataclass(frozen=True)
class WorkspaceDTO:
    workspace_id: str
    name: str
    active_watchlists: List[WatchlistDTO]

@dataclass(frozen=True)
class UserLayoutDTO:
    layout_id: str
    panels: List[str]
    theme: str

@dataclass(frozen=True)
class PresentationStateDTO:
    scanner_results: List[ScannerViewDTO]
    workspace: WorkspaceDTO
    layout: UserLayoutDTO
    total_opportunities: int