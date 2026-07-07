# Decision Intelligence Manifest

This document serves as the definitive operational contract for the entire AlphaGrid decision pipeline (Platforms 9 through 16).

## Platform 9: Concept Generation
- **Allowed Inputs**: GeometryDTO, FeatureSetDTO
- **Allowed Outputs**: ConceptSetDTO (with LineageDTO)
- **Decisions Produced**: Concept Existence, Relationship Topology
- **Decisions Forbidden**: Trading Signals, Methodology Evaluation
- **Registry Dependencies**: Concept Registry
- **Performance Budget**: Max Latency < 2ms per concept
- **Explainability**: Must provide semantic source mappings.

## Platform 10: Methodology Ecosystem
- **Allowed Inputs**: ConceptSetDTO
- **Allowed Outputs**: MethodologyResultDTO (with LineageDTO, FreshnessProfileDTO, ConfidenceProfileDTO, DataQualityProfileDTO)
- **Decisions Produced**: Directional Bias, Factor Confidence
- **Decisions Forbidden**: Execution Routing, Portfolio Allocation
- **Registry Dependencies**: Methodology Registry, Explainability Registry
- **Performance Budget**: Varies by Wave (e.g., Order Flow < 10ms)
- **Explainability**: Must populate EvidenceDTO strictly.

## Platform 18: Evidence & Explainability
- **Allowed Inputs**: ALL Pipeline DTOs (MethodologyResultDTO, PortfolioStateDTO, etc.)
- **Allowed Outputs**: ExplainabilityReportDTO, VisualizationRequestDTO
- **Decisions Produced**: Semantic Explanations, Conflict Resolution Narrative
- **Decisions Forbidden**: Generating Net-New Trading Recommendations, Recalculating Math
- **Registry Dependencies**: Explainability Registry
- **AI Permissions**: Read-Only access via Platform 22. AI cannot bypass P18 logic.
- **Human Approval**: Not required for explainability generation, but explanations support manual trade approval.