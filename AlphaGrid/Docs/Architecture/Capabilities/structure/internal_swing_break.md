# Capability Specification: Internal Swing Break

## Purpose
Detects the breakage of internal structural nodes (minor swings that reside within the current external structural leg). This provides the earliest objective indication of local order flow shifts.

## Inputs
*   **Required Dependencies:** Market Data (OHLCV)
*   **Required Evidence:** `StructureState` (Specifically `internal_highs` and `internal_lows`)

## Outputs
*   **Produced Events:** `InternalSwingBreakEvent` (EventEvidenceDTO)
*   **Interpretation Level:** `OBJECTIVE`

## Dependencies
*   `StructureDetector` -> `InternalSwingBreakEvent` -> `StructureLifecycleEngine` -> `StructureState`

## Forbidden Dependencies
*   Methodology interpretations (e.g. Internal BOS).
*   Liquidity logic, FVG, OB, Session boundaries.
*   Invalidation logic inside the detector.

## Invariants
*   Cannot occur without a valid internal swing node existing in the `StructureState`.
*   The break must be confirmed by the closing price (not just a wick).
*   Must reference the exact `state_id` of the swing node that was broken.
*   Detector must never mutate the `StructureState`.
*   Deterministic execution for a given market dataset.

## Failure Modes
*   **Wick Breaks:** A wick that breaches an internal swing but closes back inside the range is NOT an internal swing break.
*   **Simultaneous Breaks:** A single massive bar that breaks multiple internal swings should emit multiple `InternalSwingBreakEvent` streams, sequenced by depth.

## Edge Cases
*   **Equal Closes:** A close exactly equal to the swing extreme is not a break. The price must close strictly beyond the extreme.

## Acceptance Criteria
*   Correctly distinguishes between internal wicks and structural closes.
*   The Lifecycle Engine accurately consumes the event and updates the `break_history` and active nodes of the `StructureState`.
*   Mapped correctly in `concept_mapping_registry.yaml` for downstream methodologies (e.g., mapped to Internal BOS for ICT).

## Golden Dataset Coverage
*   `golden_dataset/structure/positive/internal_swing_break.json`
*   `golden_dataset/structure/negative/internal_swing_break.json`
*   `golden_dataset/structure/edge_cases/internal_swing_break.json`
