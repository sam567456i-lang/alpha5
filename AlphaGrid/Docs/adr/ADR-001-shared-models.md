---
Document ID: DOC-019
Title: "ADR-001: Shared Models Strategy"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: adr
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-03
Dependencies: []
Referenced By: []
---

# ADR-001: Shared Models Strategy

## Context
AlphaGrid is a desktop-first quantitative trading assistant with components spanning python backends (AI models, data pipelines, strategies) and frontend user interfaces (React/TypeScript). Communicating between these layers requires clear, immutable, and validated data schemas to prevent bugs, sync failures, or contract drift.

## Decision
We establish the `Shared` Python module as the authoritative source of truth for all domain models, DTOs, and enums. 

We adopt the following guidelines:
1. **Single Source of Truth**: All models must be defined once using Python Pydantic v2. Database ORMs, APIs, AI predictions, and Frontend components must map to or utilize these models.
2. **Domain-Driven Organization**: Models are divided into domain-specific modules (`market.py`, `recommendation.py`, `portfolio.py`, etc.) instead of a monolithic file, keeping the codebase modular and readable.
3. **Auto-Generated TypeScript Interfaces**: To maintain consistency between frontend and backend without manual copy-paste errors, TypeScript types are compiled directly from Python Pydantic models to `Shared/generated/`.

## Consequences
* **Pros**:
  * 100% guarantee of contract alignment between frontend and backend.
  * Extensible and organized domain structure.
  * Centralized validation logic ensures data integrity.
* **Cons**:
  * Changing a schema requires running a generation script to sync the frontend.
