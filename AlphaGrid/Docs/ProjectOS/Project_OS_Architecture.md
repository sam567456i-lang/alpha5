# Project OS Architecture Specification (Stage 5A)

## Mission
Project OS is the standalone institutional repository operating system that governs the AlphaGrid repository. It operates completely out-of-band from `Backend/` and enforces strict deterministic governance via automated audits.

## 1. Module Architecture
The Project OS engine is organized into exactly 16 independent, non-monolithic modules:
- `cli/`: Deterministic routing and argument parsing.
- `core/`: Core runtime configuration and logging.
- `scanner/`: Read-only ingestion of repository files (YAML, MD, PY).
- `repository/`: Validates repository state, hash manifests, and purity.
- `governance/`: Validates compliance with `Project_Bible.md` and Constitutions.
- `registry/`: Schema-validated ingestion of all registries (capabilities, taxonomy).
- `taxonomy/`: Taxonomy resolution engine.
- `dependency/`: DAG generator for mapping dependencies across components.
- `architecture/`: Validates structural purity against Platform rules.
- `capability/`: Resolves and builds the capability matrix.
- `validator/`: Cross-references components against the Validation Registry.
- `planner/`: Generates missing capability reports and roadmaps.
- `reporter/`: Emits dual-format (MD/JSON) governance output.
- `certification/`: Enforces the absolute E2E certification gates.
- `freezer/`: Generates immutable repository freeze reports.
- `utils/`: Safe YAML/JSON parsers.

## 2. Interfaces & Contracts
Project OS interacts with the repository strictly as **data**. It does not import AlphaGrid modules.
- **Input Contract:** Must successfully parse `master_capability_registry.yaml`, `taxonomy.yaml`, and `universal_switches.yaml`.
- **Output Contract:** Dual-format reporting (`Docs/Reports/*.md` and `Docs/Reports/*.json`).

## 3. Configuration & Schemas
- **Registry Schema**: Project OS will validate registries using strict JSON Schema validation before processing. Missing required fields (`dto`, `execution_context`) will halt the parser.
- **Report Schema**: Every generated JSON report will conform to a schema defining `timestamp`, `version`, `commit_hash`, and the report payload, guaranteeing dashboards can ingest them safely.

## 4. CLI Design
`project_os <command> [options]`
- `project_os audit`: Executes the 30+ domain repository audit.
- `project_os validate`: Executes Stage 1B validation and inconsistencies check.
- `project_os matrix --type capability`: Generates the Master Capability Matrix.
- `project_os matrix --type dependency`: Generates the Master Dependency Matrix.
- `project_os switches`: Generates the Universal Switch Registry.
- `project_os certify`: Runs the stringent E2E and Certification manifest tests.
- `project_os freeze`: Outputs the final freeze snapshot.
