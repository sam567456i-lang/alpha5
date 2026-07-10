---
Authority: Level 1
Parent: Constitution.md
Children: None
Supersedes: None
Version: 1.0.0
Status: ACTIVE
---

# Development Playbook

This playbook defines how contributors interact with the AlphaGrid ecosystem, ensuring architectural drift is mathematically eliminated.

## The Decision Ladder

Before implementing a new capability, you must ask these questions in order. You may only proceed down the ladder if all previous answers are "No".

1. **Can this be solved by configuration?**
2. **Can it be solved by a Profile?**
3. **Can it be solved by a Policy?**
4. **Can it be solved by a Projection?**
5. **Can it be solved by adding objective evidence to Platform 10?**
6. **Can it be solved by a Cross-Cutting Service?**
7. **Does it belong in an existing Program?**
8. **Does it belong in an existing Platform?**

*Only if all fail should you consider proposing architectural changes via an ADR.*

## Family Design Specifications

Before implementing *any* new capability family, you MUST draft and approve a formal specification document (e.g., `Platform10/Liquidity/Liquidity_Spec.md`). 

Every specification must explicitly define:
- Purpose
- Scope
- Inputs (Required features, timeframes, data types)
- Outputs (Produced evidence)
- Dependencies
- Consumers (Methodologies, Policies, Learning)
- Complexity & Computational Cost
- Performance Target
- Test Plan (Unit, Integration, Replay)
- Certification Checklist

Code implementation may only begin once this specification reaches **CRL-2 (Specification)** status.

## Pull Request Rejection Criteria

A PR **must** be rejected if it:
1. Violates the Constitution (e.g., Platform 11 modifying Platform 10 evidence).
2. Uses `datetime.now()` instead of tick-driven time context, breaking replayability.
3. Implements an architectural change without an approved ADR.
4. Bypasses the SDK contracts to directly access underlying memory structures.
5. Blurs the line between Objective Measurement and Subjective Interpretation.
