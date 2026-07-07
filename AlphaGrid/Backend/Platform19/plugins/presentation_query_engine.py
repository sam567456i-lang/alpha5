from Backend.Platform19.contracts.dtos import (
    PresentationQueryDTO, PresentationStateDTO, ScannerViewDTO, 
    WorkspaceDTO, WatchlistDTO, UserLayoutDTO
)
from Backend.Platform10.contracts.dtos import MethodologyResultDTO
from typing import List

class PresentationQueryEngine:
    def execute(self, query: PresentationQueryDTO, raw_opportunities: List[MethodologyResultDTO]) -> PresentationStateDTO:
        # 1. Apply Semantic Filters
        filtered = [
            opp for opp in raw_opportunities
            if opp.confidence >= query.semantic_filters.confidence_min
        ]
        
        # 2. Apply Default or Requested Sorting
        # Example default: Confidence DESC
        filtered.sort(key=lambda x: x.confidence, reverse=True)
        
        # 3. Apply Pagination
        start = (query.page - 1) * query.page_size
        end = start + query.page_size
        paged = filtered[start:end]
        
        # 4. Map to Presentation Model (ScannerViewDTO)
        scanner_results = []
        for opp in paged:
            scanner_results.append(ScannerViewDTO(
                opportunity_id=opp.execution_id,
                symbol="AAPL", # Mocked mapping
                confidence_display=f"{int(opp.confidence * 100)}%",
                freshness_display="Fresh", # Mocked
                primary_evidence="Semantic Evidence Extracted",
                risk_level="Low"
            ))
            
        # 5. Assemble Subsystems
        workspace = WorkspaceDTO(query.active_workspace_id, "Default Workspace", [])
        layout = UserLayoutDTO(query.active_layout_id, ["Scanner", "Chart"], "Dark")
        
        return PresentationStateDTO(
            scanner_results=scanner_results,
            workspace=workspace,
            layout=layout,
            total_opportunities=len(filtered)
        )