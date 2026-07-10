# The AlphaGrid Quantitative Research Constitution v1.1

The architectural design phase of AlphaGrid is complete. This document serves as the immutable constitution governing all future quantitative research. 

## Article I: The Immutable Boundaries
Information flows forward. It never leaks backward. Every platform executes exactly one responsibility.
- **Platform 10**: Objective mathematical **Measurements**.
- **Phase 3 Library**: Atomic Research **Hypotheses**.
- **Platform 11**: **Evidence-based Interpretive Claims**.
- **Platform 12**: **Decision** Intelligence.

**Rule of Ownership**: A downstream platform may consume upstream outputs but must never recompute or reinterpret upstream responsibilities. 

## Article II: The Rule Specifications
Research intent must outlive code implementation. Every rule in the library must consist of:
1. `RuleName.py` (The implementation)
2. `RuleName.spec.md` (Objective, Mathematical definition, Inputs, Outputs, Failure modes, Validation history)

## Article III: Two-Dimensional Maturity
A rule's maturity is tracked across two completely independent axes:
- **Engineering Maturity** (*Can I trust the software?*): `Draft` -> `Implemented` -> `Unit Tested` -> `Golden Certified` -> `Laboratory Certified`
- **Research Maturity** (*Can I trust the hypothesis?*): `Research` -> `Candidate` -> `Validated` -> `Production` -> `Deprecated`

**Promotion Law**: Promotion along one maturity axis never implies promotion along the other.

## Article IV: The Dependency Hierarchy
Rules are developed in strictly ordered dependency layers (Primitives -> Structural -> Confirmation -> Composite). 
**DAG Preservation Law**: Every rule may depend only on its own layer or lower layers. Circular dependencies are prohibited.

## Article V: The Engineering Loop
Research is iterative. Every hypothesis progresses through:
`Implement -> Unit Test -> Golden Validate -> Stress Validate -> Evaluate Detection Quality -> Specification Review -> Walk-Forward -> Promote / Revise / Reject`
**Success Definition**: A rejected hypothesis is a successful research outcome if it prevents future capital allocation to a false idea.

## Article VI: Multi-Dimensional Coverage
Progress is measured by establishing robust research coverage across Domains, Asset-Classes, and Market-Regimes, not arbitrary rule counts.

## Article VII: The Supreme Mandate
*No hypothesis is accepted because it is plausible, elegant, or widely believed. It is accepted only because it survives empirical validation on reproducible data under the defined promotion criteria.*

## Article VIII: Reproducibility & Immutability
Every published research result must be reproducible, explicitly recording Rule version, Dataset version, Platform version, Configuration, and Random seed. 
**Immutability Law**: Research artifacts are immutable. Corrections create new versions; they never overwrite historical records.

## Article IX: Falsifiability
Every rule specification must define expected success cases, expected failure cases, and conditions under which the hypothesis is considered disproven.

## Article X: Objective First Principle
Every component must publish the most objective representation possible (e.g., publish `LiquidityLevel`, not `Stop Hunt`).

## Article XI: The Experiment Ledger
Every experiment, regardless of outcome, must be permanently recorded in a centralized **Experiment Ledger**. The ledger must track the Experiment ID, Target Hypothesis, Empirical Result (Promoted/Revised/Rejected), and the quantitative Reason. This guarantees AlphaGrid learns from its failures and prevents the resurrection of statistically disproven ideas.
