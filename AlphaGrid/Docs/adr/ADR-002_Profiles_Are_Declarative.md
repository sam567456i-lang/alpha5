# ADR-002: Profiles Are Declarative

## Status
Accepted - Frozen (Platform 11 Constitution)

## Context
As the number of methodology variants grows (e.g., ICT 2022, ICT Conservative, Wyckoff Accumulation), hardcoding configurations into Python logic leads to unmanageable code sprawl and prevents researchers from safely modifying methodology parameters without software engineering intervention.

## Decision
Methodology profiles must be purely declarative (YAML/JSON). They support inheritance to allow composition of complex rulesets from base definitions without duplicating code. Python is reserved strictly for executing reusable logic (Evaluators).

## Consequences
- **Positive:** Enables researchers to compose and tweak methodologies without writing code. Drastically improves configuration traceability.
- **Negative:** Requires a robust `ProfileLoader` and compile-time DAG builder (`FrozenPolicyPlan`) to translate configurations into execution paths.
