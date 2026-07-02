# AlphaGrid Constitution

## Mandatory Institutional-Grade Engineering Standard

> **NON-NEGOTIABLE REQUIREMENT**

Every implementation produced for AlphaGrid—across every phase, slice, module, feature, concept, methodology, strategy, experiment, and production subsystem—**must be institutional-grade, production-ready software**. This requirement applies to the entire project without exception.

Prototype code, placeholder implementations, proof-of-concepts, demonstration code, simplified examples, temporary workarounds, shortcuts, duplicated logic, or "good enough" implementations are strictly prohibited.

Every implementation must satisfy the following standards before it is considered complete.

### Architecture
* Strictly follow the AlphaGrid Constitution.
* Preserve the frozen architecture unless an architectural change is explicitly approved.
* Follow SOLID principles.
* Follow Clean Architecture principles.
* Maintain strict downward dependency flow.
* No circular dependencies.
* Single Source of Truth for every calculation.
* Reuse existing infrastructure rather than creating parallel implementations.
* Extend the platform through generic abstractions instead of indicator-specific or methodology-specific code.

### Code Quality
* Production-grade implementation only.
* Institutional-quality engineering suitable for long-term maintenance.
* Fully typed with comprehensive Python type hints.
* Small, cohesive, single-responsibility classes and modules.
* Clear separation of responsibilities.
* Dependency Injection where appropriate.
* Immutable objects where appropriate.
* Deterministic behavior.
* Readable, maintainable, and well-documented code.
* No magic numbers or magic strings.
* No duplicated business logic.
* No dead code.
* No commented-out code.
* No TODO or FIXME placeholders.
* No hidden side effects.

### Reliability
* Comprehensive input validation.
* Domain-specific exception hierarchy.
* Fail-fast behavior.
* Explicit error handling.
* No silent failures.
* Deterministic execution.
* Thread-safe where applicable.
* Backward-compatible public interfaces unless explicitly approved.

### Performance
* Prioritize correctness and maintainability before optimization.
* Streaming O(n) algorithms where appropriate.
* Avoid unnecessary allocations.
* Eliminate duplicated calculations.
* Reuse cached computations through the Feature DAG.
* Prevent duplicate feature execution.
* Benchmark performance-critical components when appropriate.

### Mathematical Correctness
* Every algorithm must be verified against known-value reference vectors or trusted implementations where appropriate.
* Validate boundary conditions.
* Validate warm-up behavior.
* Validate missing-data handling.
* Validate floating-point tolerance where applicable.
* Scientific correctness is mandatory before promotion.

### Testing
Every implementation must include appropriate verification.
* Unit tests
* Integration tests
* Family integration tests
* Deterministic regression tests
* Mathematical verification tests
* Dependency graph verification
* Edge-case testing
* Failure-path testing

Passing tests are required but do not, by themselves, prove production readiness.

### Production Acceptance Criteria
No implementation may be merged or marked complete until all of the following have been verified:
* Architecture compliance
* Repository-wide dependency integrity
* Mathematical correctness
* Deterministic execution
* Performance acceptance
* Static analysis and type checking
* Documentation completeness
* Unit tests passing
* Integration tests passing
* Scientific validation requirements satisfied
* No known architectural defects
* No known correctness defects
* No known maintainability issues

### Repository Audit (Mandatory)
Every completed slice must undergo a repository-wide engineering audit before approval.
The audit must verify:
* Architecture compliance
* SOLID compliance
* Clean Architecture compliance
* Dependency integrity
* Code quality
* Type safety
* Performance
* Error handling
* Testing completeness
* Documentation quality
* Research governance compliance

Every finding must be either:
* Fixed, or
* Explicitly documented and accepted before the slice is considered complete.

### Engineering Principle
AlphaGrid is intended to be an institutional-quality quantitative research platform.
Every contribution must be written as if it will be maintained, extended, audited, and deployed in a professional production environment for many years.

**Institutional-grade engineering is mandatory for the entire project and is not optional. Quality requirements must never be relaxed for speed or convenience.**

---

## AI Code Generation Rules
When generating code:
- Generate complete implementations, never skeletons.
- Never leave TODOs, FIXME comments, or placeholder methods.
- Never omit edge-case handling.
- Never simplify because of response length.
- Generate production-quality code suitable for a real-world trading platform.
- If output exceeds a single response, continue automatically until the implementation is complete.
- Prefer correctness, maintainability, determinism, and extensibility over brevity.
- Every implementation should be suitable for immediate code review and repository integration.

## Standard Research Lifecycle
Every research volume and strategy must follow this standardized template:
1. Theory
2. Research Evidence
3. Required Features (Raw measurements)
4. Required Concepts (Semantic market meaning)
5. Primitive Signals
6. Methodologies (Combination of concepts)
7. Strategies (Declarative pipelines)
8. Experiments (RH / EXP)
9. Validation (WalkForward, Monte Carlo)
10. Scientific Evaluation (Profitability, Risk, Robustness, Statistics)
11. Promotion Rules (Automated gating to Candidate Registry)

> **Note:** SMC, ICT, and Wyckoff are Methodologies, not core architectures. They must consume generic concepts.

## Scientific Evaluation
- Every experiment must produce a complete evaluation report.
- The evaluation report is the sole source of truth for strategy quality.
- Strategies are promoted only through the Promotion Engine.
- Individual metrics must never be evaluated independently.
- Promotion decisions are based on the complete evaluation profile.
