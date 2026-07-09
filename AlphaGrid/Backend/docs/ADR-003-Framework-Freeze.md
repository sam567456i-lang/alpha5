# ADR 003: Framework Infrastructure Freeze & Semantic Invariants

## Context
Platform 10 has achieved maturity in its architectural foundation (Wave 2B.1A). The separation between evidence production and interpretation is robust. The graph-based structural representation is strictly deterministic. Replay architectures, identity generation, and registry governance are in place. To prevent continuous abstraction expansion that delays capability delivery, we are officially freezing the framework infrastructure.

## Decision

1. **Framework Freeze**: No new framework abstractions shall be added to Platform 10 unless a concrete capability implementation cannot be completed within the existing architecture. Any unblocking abstraction must be explicitly documented and approved via an ADR. The highest return on effort is now implementing and certifying the Tier 1 rule library (Structure, Liquidity, Imbalance, Institutional Zones, Range, Auction, Delivery).

2. **Immutable Graph Snapshots**: `StructureGraphSnapshotDTO` instances are append-only historical records. They must never be regenerated or mutated. Replay and UI state updates must consume `StructureGraphDeltaDTO` to transition between snapshots.

3. **Event Sourcing as Canonical Truth**: The platform operates on event sourcing. `EventEvidenceDTO` (and descendants like `SwingFormationEvent`, `BreakEventDTO`) are the absolute, canonical source of truth. `StateEvidenceDTO` (e.g. `StructureState`) are merely materialized views derived from processing these events sequentially.
    - If a state is lost, it can be mathematically re-materialized via the `LifecycleEngine`.
    - If an event is lost, history is corrupted.

## Consequences
- Developers will focus entirely on implementing objective Stage 1-4 capabilities and Methodology plugins.
- Graph traversal logic is stabilized using `node_type` and `edge_type` registry IDs.
- Future capabilities that require new graph shapes will map into the existing `StructureGraphDTO` via new namespaces (e.g. `imbalance/default`).
