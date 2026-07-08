# ADR-007: Universal Zone Framework

## Context
As the spatial framework scales to handle order blocks, fair value gaps, breakers, and volume profiles, hardcoding these as subclassed detectors leads to immense code duplication and object-oriented complexity.

## Decision
We have decided to build a **Unified `ZoneDTO`**, replacing subclasses (like `GapZoneDTO`, `BlockZoneDTO`) with a single, completely registry-driven spatial entity. 

## Architectural Principles
1. **Composition over Inheritance**: Detectors no longer encapsulate geometry logic. Instead, a `ZoneDetectorBase` orchestrates discrete engines (`MergeEngine`, `OverlapEngine`, `LifecycleEngine`) based on registry instructions.
2. **Stateless Operations**: Detectors are stateless. The state machine (PENDING, DETECTED, CONFIRMED, ACTIVE, MITIGATED, INVALIDATED, ARCHIVED) is completely delegated to `Docs/Governance/registry/zone_state_machine_registry.yaml`.
3. **Index Abstraction**: Direct list-iteration searches are deprecated in favor of an abstract `ZoneIndex` interface. This allows future swapping to an `RTree` or `IntervalTree` without detector changes.
4. **Mandatory Metadata**: All operational, explainability, lineage, and capability-mapping characteristics are rigidly stored inside `ZoneMetadataDTO`, rather than relying on class typing.

## Consequences
- **Positive**: We can now define infinite spatial concept derivatives without writing new geometry math. Memory overhead is strictly bounded and benchmarked to O(1) or O(N) constraints per the performance budgets.
- **Negative**: The YAML registries are highly complex and must be rigidly validated at startup using robust certification and validation logic.

## Related ADRs
This framework relies heavily on previous architectural decisions. See the following for complete context:
- **Detector Framework ADR**: Orchestration and composition rules.
- **DTO Framework ADR**: Immutable data transfer constraints.
- **Registry ADR**: Rules for file-based configuration.
- **Ontology ADR**: Mapping zones to abstract trading concepts.
- **Structure FSM ADR**: Foundational state machine principles inherited by zones.
