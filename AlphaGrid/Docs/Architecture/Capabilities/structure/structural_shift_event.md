# Capability Specification: Structural Shift Event

## Purpose
Detects a broader shift in market mechanics, often serving as a higher-confidence secondary confirmation following a `TrendReversalEvent`. While a Trend Reversal breaks the immediate origin, a Structural Shift indicates the failure of major, multi-leg structural complexes.

## Inputs
*   **Required Dependencies:** Market Data (OHLCV)
*   **Required Evidence:** `StructureState` (Specifically tracking major, higher-degree structural pivots)

## Outputs
*   **Produced Events:** `StructuralShiftEvent` (EventEvidenceDTO)
*   **Interpretation Level:** `DERIVED`

## Dependencies
*   `StructuralShiftDetector` -> `StructuralShiftEvent` -> `StructureLifecycleEngine` -> `StructureState`

## Forbidden Dependencies
*   Purely subjective methodologies (e.g. MSS).
*   Invalidation logic inside the detector.

## Invariants
*   Must reference a major, multi-leg complex or higher-degree pivot defined in `StructureState`.
*   The break must be confirmed by the closing price (not just a wick).
*   Must reference the exact `state_id` of the major pivot that was broken.
*   Detector must never mutate the `StructureState`.
*   Deterministic execution for a given market dataset.

## Failure Modes
*   **Wick Breaks:** A wick that breaches a major structural complex but closes back inside is NOT a structural shift.
*   **Overlap with Trend Reversal:** A Structural Shift and a Trend Reversal can occasionally occur on the same bar if the structural leg is extremely condensed. The detector must accurately emit both events independently if criteria are met.

## Edge Cases
*   **Equal Closes:** A close exactly equal to the major complex extreme is not a shift. The price must close strictly beyond the extreme.

## Acceptance Criteria
*   Accurate segregation from `TrendReversalEvent`.
*   The Lifecycle Engine accurately consumes the event and rebuilds the `StructureState` to align with the new major paradigm, marking previous major topologies as invalidated.
*   Mapped correctly in `concept_mapping_registry.yaml` for downstream methodologies (e.g., mapped to MSS for ICT).

## Golden Dataset Coverage
*   `golden_dataset/structure/positive/structural_shift_event.json`
*   `golden_dataset/structure/negative/structural_shift_event.json`
*   `golden_dataset/structure/edge_cases/structural_shift_event.json`
