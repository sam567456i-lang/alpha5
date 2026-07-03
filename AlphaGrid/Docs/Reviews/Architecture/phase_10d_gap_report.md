---
Document ID: REV-006
Title: "Phase 10D Gap Report: Concept Domain"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: Reviews
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-03
Dependencies: []
Referenced By: []
---

# Phase 10D Gap Report: Concept Domain

## 1. Existing Concept Generators (Functional)
The following concept generators are currently implemented as `AbstractConceptGenerator` classes and are correctly integrated into the `ConceptRegistry` and `canonical_pipeline`. They correctly consume `feature_values` outputted by the Feature Engine:
- `BreakoutConceptGenerator`
- `ExtremumConceptGenerator`
- `MomentumConceptGenerator`
- `StrengthConceptGenerator`
- `TrendConceptGenerator`
- `VolatilityConceptGenerator`
- `VolumeConceptGenerator`

**Status:** These are production-ready but rely entirely on Feature outputs. They do not consume Geometry.

## 2. Disconnected / Legacy Concept Engines
The following engines exist in the codebase but are completely bypassed by the `canonical_pipeline`. They do not conform to the `AbstractConceptGenerator` contract.
- `PriceActionEngine`: Computes candlestick patterns natively from raw OHLC data, bypassing both the Feature Engine and Geometry Graph.
- `SMCEngine`: Computes Order Blocks by directly querying the `GeometryGraph` for FVGs and Structure (BOS/CHOCH), bypassing the unified Concept Engine pipeline completely.

**Status:** Both of these are legacy engines. They violate the Canonical Runtime Contract and the Universal Engine Contract because they operate independently outside the pipeline and consume data from disallowed layers. 

## 3. The Geometry-Concept Gap
Currently, the canonical `ConceptEngine.process()` method only accepts `feature_values` as input:
```python
def process(self, timestamp: datetime, feature_values: Dict[str, Any]) -> Dict[str, Concept]:
```
It does not accept a `geometry_cache` or `geometry_graph`. Therefore, for Market Structure concepts (SMC, Wyckoff) to be computed within the canonical Concept Engine, we must refactor `ConceptEngine` and `AbstractConceptGenerator` to accept `geometry_cache` / `graph` as an input dependency, just as we did for the Feature Engine.

## 4. Test Coverage Gap
Currently, the tests mapped to concepts are:
- `Tests/test_concept_engine.py`
- `Tests/concepts/test_concept_registry.py`
- `Tests/concepts/test_smc_translation.py`

There are no tests for Price Action, Wyckoff, AMT, ICT, or Volume Profile.

## 5. Refactoring Plan for 10D
To integrate 10D cleanly without violating the Architecture Bible:
1. Deprecate `AbstractConceptEngine`, `PriceActionEngine`, and `SMCEngine`.
2. Refactor `AbstractConceptGenerator` to accept `geometry_cache` as an input alongside `feature_values`.
3. Re-implement Price Action and SMC as `AbstractConceptGenerator` subclasses so they are automatically registered and executed sequentially inside the canonical pipeline.
4. Build new Generators for Wyckoff, AMT, and ICT.
