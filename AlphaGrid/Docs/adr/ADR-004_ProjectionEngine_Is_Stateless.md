# ADR-004: ProjectionEngine Is Stateless

## Status
Accepted - Frozen (Platform 11 Constitution)

## Context
As multiple downstream consumers require different views of methodology interpretations (e.g., Narrative string, Dashboard JSON, Decision DTO), there is a risk of modifying the core `InterpretationGraph` to accommodate rendering logic.

## Decision
The `ProjectionEngine` is strictly stateless. It may read from the `InterpretationGraph`, but it is constitutionally forbidden from creating persistent nodes or mutating the graph. Projections are ephemeral views/DTOs mapped for specific downstream domains (e.g., `NarrativeProjection`, `LLMProjection`).

## Consequences
- **Positive:** Protects the integrity and immutability of the `InterpretationGraph`. Ensures that rendering logic never bleeds back into evaluation logic.
- **Negative:** Requires projections to recalculate or map data every time they are requested.
