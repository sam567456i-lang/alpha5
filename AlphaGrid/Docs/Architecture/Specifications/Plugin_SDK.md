# Plugin SDK Specification
*AlphaGrid Mandatory Infrastructure Framework 3/5*

AlphaGrid scales laterally via dynamic plugin architectures. Whether extending P10 (Methodologies), P15 (Risk Engines), or P16 (Portfolio Allocation), all plugins must adhere to this SDK specification to prevent architectural drift.

## 1. Plugin Lifecycle
Every plugin must expose hooks for the following lifecycle states:
1. **Registered**: Found in `plugin_registry.yaml` and loaded into the plugin host.
2. **Initialized**: Configuration injected, validated, and cached.
3. **Prepared**: Subscribed to relevant data dependencies (e.g. required features).
4. **Executed**: The core `analyze()` or `execute()` payload is invoked.
5. **Teardown**: Graceful shutdown and memory release.

## 2. Plugin Contract (Python ABC)
Plugins MUST inherit from a formal Abstract Base Class (ABC) defined by the owner platform.
* The plugin MUST declare its exact dependencies (e.g., `requires_features = ["RSI_14", "VWAP"]`).
* The plugin MUST accept exactly one immutable Input DTO.
* The plugin MUST return exactly one immutable Output DTO (or raise a tracked Governance Error).
* Plugins are forbidden from performing external I/O (No DB, No Broker API, No Sockets) during their execution block.

## 3. Registration & Discovery
All plugins exist in the `plugin_registry.yaml`.
* **ID**: Unique identifier.
* **Owner**: The platform running it.
* **Path**: Import path to the implementation.
* **Version**: Semantic versioning.

## 4. Certification and Version Compatibility
ProjectOS will automatically reject any plugin that fails:
* Unit tests (mandatory).
* Determinism testing (yielding the same output for same inputs).
* Performance budget (must execute within max latency allowed for its plugin category).
* Backward compatibility: If a plugin upgrades to `v2.0`, it must guarantee `v1.0` logic does not break existing test baselines unless explicitly marked as a breaking schema change.
