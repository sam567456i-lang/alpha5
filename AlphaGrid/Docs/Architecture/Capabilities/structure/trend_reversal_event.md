# Capability Specification: Trend Reversal Event

## Purpose
Detects the first objective indication of a potential major topographic shift in the market. This occurs when price violates the structural origin that created the most recent `ExternalSwingBreakEvent`.

## Inputs
*   **Required Dependencies:** Market Data (OHLCV)
*   **Required Evidence:** `StructureState` (Requires preceding External Swing Break events and tracking of protected origin nodes)

## Outputs
*   **Produced Events:** `TrendReversalEvent` (EventEvidenceDTO)
*   **Interpretation Level:** `DERIVED`

## Dependencies
*   `TrendReversalDetector` -> `TrendReversalEvent` -> `StructureLifecycleEngine` -> `StructureState`

## Forbidden Dependencies
*   Methodology interpretations (e.g. CHOCH, Accumulation/Distribution).
*   Moving averages, oscillators.
*   Invalidation logic inside the detector.

## Invariants
*   Cannot occur without a valid protected origin node existing in the `StructureState`.
*   The break must be confirmed by the closing price (not just a wick).
*   Must reference the exact `state_id` of the protected origin node that was broken.
*   Detector must never mutate the `StructureState`.
*   Deterministic execution for a given market dataset.

## Failure Modes
*   **Internal vs External:** Breaking an internal swing is an Internal Swing Break, NOT a Trend Reversal Event. A Trend Reversal strictly refers to the failure of the major structural leg's protected origin.
*   **Sweep of Origin:** If the origin is wick-swept but not closed below, it is an aggressive sweep, not a Trend Reversal Event.

## Edge Cases
*   **Equal Closes:** A close exactly equal to the protected origin extreme is not a reversal. The price must close strictly beyond the extreme.

## Acceptance Criteria
*   Must strictly validate that the broken node was the origin of a prior validated `ExternalSwingBreakEvent`.
*   The Lifecycle Engine accurately consumes the event and marks the entire prior structural leg as superseded/invalidated.
*   Mapped correctly in `concept_mapping_registry.yaml` for downstream methodologies (e.g., mapped to CHOCH for ICT).

## Golden Dataset Coverage
*   `golden_dataset/structure/positive/trend_reversal_event.json`
*   `golden_dataset/structure/negative/trend_reversal_event.json`
*   `golden_dataset/structure/edge_cases/trend_reversal_event.json`
