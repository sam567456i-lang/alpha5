# ADR-001: Evidence Is Immutable

## Status
Accepted - Frozen (Platform 10 Constitution)

## Context
As the methodology engines (Platform 11) and decision engines (Platform 12) consume market data, there is a risk that different methodologies might alter or interpret base data differently in place, leading to non-deterministic behavior and breaking replayability.

## Decision
Platform 10 objective `Evidence` objects are strictly immutable. They cannot be modified by any downstream process. Once created, they represent a permanent historical record of an objective fact (e.g., a tick, an event, a relationship) at a precise moment in time.

## Consequences
- **Positive:** Guarantees absolute replay determinism. Methodologies can safely share the same `EvidenceGraph` without side effects.
- **Negative:** Requires creating new Interpretation objects downstream rather than enriching existing objects, increasing memory overhead slightly.
