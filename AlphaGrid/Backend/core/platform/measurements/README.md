# Platform 10: Measurement Framework

## Core Philosophy
Platform 10 is the singular authoritative source of objective facts within AlphaGrid. It isolates strict mathematical measurements from predictive hypotheses. 

**What Platform 10 Is**: An extensible library of pure mathematical measurements that emits immutable, deterministic, and highly traceable features, objects, and events.
**What Platform 10 Is Not**: A hypothesis engine. It does not contain semantic logic (e.g., "Support", "Resistance", "Break of Structure", "Fair Value Gap", "Trending", "Ranging").

## API Guarantees & Stability
**Platform 10 public interfaces are frozen.** Existing measurement contracts (input schemas, output schemas, causality, provenance) are versioned and considered stable.
Modifying an existing measurement contract requires a version bump.

## Measurement Admission Criteria
New measurements may be added to the catalog in the future **only if** they are justified by empirical research and satisfy the following criteria:
1. **Objective**: The calculation must be purely mathematical.
2. **Deterministic**: Given identical inputs and configurations, the output must be identical.
3. **Causal**: The measurement must strictly define its causality (`ONLINE` vs `OFFLINE`).
4. **Authoritative**: There must be exactly one implementation of the measurement algorithm in the repository.
5. **Reusable**: At least three independent future hypotheses must plausibly consume this measurement. (If a measurement is highly specialized to a single hypothesis, it belongs in Phase 3).
6. **No Semantic Logic**: Convenience features like `FreshnessScore`, `PersistenceScore`, or `ReactionScore` are strictly forbidden. Publish only primitive facts (e.g., `Timestamp` or `FormationBar`).

## Causality Definitions
Platform 10 formally segregates measurements by causality to protect live trading integrity:
- **`ONLINE`**: Strictly causal. Operates solely on current and past data (e.g., Trailing ATR, Touch Events). Safe for streaming.
- **`OFFLINE`**: Requires future data (e.g., Centered Pivots). Restricted to historical batch research. The `StreamingAdapter` will fatally reject any `OFFLINE` engine.

## Versioning & Deprecation Policy
- Changes to the underlying algorithm that alter the output array necessitate a new `implementation_version`.
- Deprecated measurements will be marked in the `MeasurementRegistry`, but legacy code will be retained until all consuming Phase 3 rules have been migrated or retired.

## How to Add a New Measurement
1. Define the mathematical primitive in the appropriate family (`objects/`, `events/`, or `features/`).
2. Inherit from `MeasurementEngine` and define `measurement_type`, `implementation_version`, and `causality`.
3. Expose the API schema in `registry.py`.
4. Ensure the output `Dict` contains the full `provenance` metadata.
5. Add rigorous `test_p7.py` assertions for Replay Serialization, Idempotence, and Equivalence (if `ONLINE`).
