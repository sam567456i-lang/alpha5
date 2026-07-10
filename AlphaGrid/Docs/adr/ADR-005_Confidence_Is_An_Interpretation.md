# ADR-005: Confidence Is An Interpretation

## Status
Accepted - Frozen (Platform 11 Constitution)

## Context
Methodologies express varying levels of confidence in their evaluations. Initially, confidence was modeled as a scalar field (e.g., `confidence=82`) on a base Interpretation object. However, confidence itself is a subjective methodology calculation. ICT might calculate confidence differently than Wyckoff or AMT, rendering a shared scalar field mathematically meaningless.

## Decision
Confidence is decoupled from the base fields and elevated to its own interpretation class: `ConfidenceInterpretation`. It belongs to the `InterpretationGraph` identically to any other subjective node, carrying its own provenance and methodology tracing.

## Consequences
- **Positive:** Enables scaling multiple methodologies safely. Downstream engines (Platform 12) can parse confidence strictly in the context of the methodology that generated it.
- **Negative:** Slightly increases the size of the `InterpretationGraph`.
