# Capability Specification: Swing Structure

## Purpose
Defines the highest-confidence market turning points by tracking local maxima and minima. This forms the objective topographic layer of the market that all downstream structural rules consume.

## Inputs
*   **Required Dependencies:** Market Data (OHLCV)
*   **Required Evidence:** `GeometryEvidence` (Fractal formations)
*   **Policies:** `SwingPolicy` (Determines the algorithm: e.g., N-bar confirmation, zigzag threshold, inside bar handling).

## Outputs
*   **Produced State:** `StructureState` (Specifically the mapping of `major_highs`, `major_lows`, `internal_highs`, `internal_lows`).
*   **Produced Events:** `SwingFormationEvent`
*   **Interpretation Level:** `OBJECTIVE`

## Dependencies
*   `SwingDetector` -> `SwingFormationEvent` -> `StructureLifecycleEngine` -> `StructureState`

## Forbidden Dependencies
*   Methodology interpretations (e.g. Trend, Bias, SMC Concepts).
*   Order Blocks, FVG, Liquidity computations.

## Invariants
*   Detector must never mutate state.
*   Cannot reference future candles.
*   Deterministic given identical `SwingPolicy`.
*   Cannot emit duplicate `SwingFormationEvent`s for the same fractal node.

## Failure Modes
*   **Equal Highs/Lows:** Consecutive bars with identical wick extremes must be bounded by the `SwingPolicy` to prevent duplicate swing nodes.
*   **Adaptive Failures:** If `SwingPolicy` is adaptive, extreme volatility can cause missing swings if not properly bounded.

## Edge Cases
*   **Inside Bars:** Standard behavior dictates inside bars do not form valid swings unless the parent bar is broken. The `SwingPolicy` dictates this behavior.

## Acceptance Criteria
*   Detector strictly separates state management from detection.
*   Lifecycle engine handles `SwingFormationEvent` and updates `StructureState` purely geometrically.

## Golden Dataset Coverage
*   `golden_dataset/structure/positive/swing.json`
*   `golden_dataset/structure/negative/swing.json`
*   `golden_dataset/structure/edge_cases/swing_inside_bars.json`
