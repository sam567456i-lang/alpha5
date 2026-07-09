# Capability Specification: External Swing Break

## Purpose
Detects the breakage of major external structural nodes (the boundaries of the current active structural leg). This provides objective evidence of the continuation of a major market direction.

## Inputs
*   **Required Dependencies:** Market Data (OHLCV)
*   **Required Evidence:** `StructureState` (Specifically `major_highs` and `major_lows`)

## Outputs
*   **Produced Events:** `ExternalSwingBreakEvent` (EventEvidenceDTO)
*   **Interpretation Level:** `OBJECTIVE`

## Dependencies
*   `StructureDetector` -> `ExternalSwingBreakEvent` -> `StructureLifecycleEngine` -> `StructureState`

## Forbidden Dependencies
*   Methodology interpretations (e.g. External BOS, Trend confirmation).
*   Liquidity logic, FVG, OB, Session boundaries.
*   Invalidation logic inside the detector.

## Invariants
*   Cannot occur without a valid external swing node existing in the `StructureState`.
*   The break must be confirmed by the closing price (not just a wick).
*   Must reference the exact `state_id` of the swing node that was broken.
*   Detector must never mutate the `StructureState`.
*   Deterministic execution for a given market dataset.

## Failure Modes
*   **Wick Breaks:** A wick that breaches an external swing but closes back inside the range is NOT an external swing break. (It may be an external sweep).
*   **Invalidated Origins:** If an External Swing Break occurs, but the origin of the move was already breached (a Trend Reversal Event), the sequence breaks. The engine must track this.

## Edge Cases
*   **Equal Closes:** A close exactly equal to the major swing extreme is not a break. The price must close strictly beyond the extreme.

## Acceptance Criteria
*   Correctly distinguishes between external wicks and structural closes.
*   The Lifecycle Engine accurately consumes the event, validates a new structural leg, protects the origin node of the new leg, and invalidates the breached node.
*   Mapped correctly in `concept_mapping_registry.yaml` for downstream methodologies (e.g., mapped to External BOS for ICT).

## Golden Dataset Coverage
*   `golden_dataset/structure/positive/external_swing_break.json`
*   `golden_dataset/structure/negative/external_swing_break.json`
*   `golden_dataset/structure/edge_cases/external_swing_break.json`
