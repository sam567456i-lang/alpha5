# Platform 5 Core Architecture

Platform 5 operates purely on the Universal Contracts and DTOs loaded directly from Governance.

## Components

1. **RegistryLoader**: Dynamically parses `master_capability_registry.yaml` at runtime to understand all available capabilities without hardcoding them.
2. **AnalysisFactory**: Instantiates the correct implementation of `BaseAnalysis` mapped to a registered `capability_id`.
3. **ContractValidator**: Ensures that any injected `AnalysisContext` and resulting `AnalysisResult` perfectly comply with the schema defined in `contracts.yaml`.
4. **AnalysisPipeline**: The core execution loop that validates input, executes analysis, and validates output.
5. **AnalysisEngine**: Handles bulk or concurrent analysis orchestration, passing valid contexts down to individual pipelines.

## DTOs

Every analysis module strictly consumes an `AnalysisContext` and returns an `AnalysisResult`. 
- `AnalysisContext` contains `market_data` (DataFrame), `timeframe` (str), `parameters` (dict), and `dependencies` (dict).
- `AnalysisResult` contains `score` (-1.0 to 1.0), `raw_data` (DataFrame), `signals` (list), and `metadata` (dict).
