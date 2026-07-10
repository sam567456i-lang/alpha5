---
Authority: Level 1
Parent: Docs/Governance/Constitution.md
Children: None
Supersedes: api_contracts.md
Version: 1.0.0
Status: ACTIVE
---

# SDK Contracts

This document formalizes the public boundaries between the six deterministic platforms.

## Invariant Rule
A platform may **only** be queried via its designated SDK object. Direct database access, scraping, or reading internal memory state from a downstream platform or supporting program is strictly forbidden.

## The Contracts

1. **`EvidenceSDK` (Platform 10)**
   - Returns immutable Evidence Graphs.
   - Used by Platform 11.

2. **`MethodologySDK` (Platform 11)**
   - Returns immutable Interpretation Graphs and Narrative Projections.
   - Used by Platform 12 and Platform 15.

3. **`DecisionSDK` (Platform 12)**
   - Returns Decision Candidates and Execution Plans.
   - Used by Platform 13 and Platform 15.

4. **`ExecutionSDK` (Platform 13)**
   - Returns live Order Sequence state and tactical portfolio tracking.
   - Used by Platform 14 and Platform 15.

5. **`LearningSDK` (Platform 14)**
   - Returns Statistics, Attribution, and ML Calibrations.
   - Used by Platform 15.
