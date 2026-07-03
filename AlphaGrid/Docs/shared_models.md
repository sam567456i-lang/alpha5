---
Document ID: DOC-017
Title: "Shared Models Module"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: Root
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-03
Dependencies: []
Referenced By: []
---

# Shared Models Module

## Purpose

The `Shared` package defines all core domain schemas, Data Transfer Objects (DTOs), and enums used across the AlphaGrid platform. It serves as the single, authoritative contract defining how the backend (FastAPI, APScheduler, AI pipelines) and frontend (React/TypeScript) exchange data.

## Ownership Rules

- **Authoritative Source**: All shared models are defined as Python Pydantic v2 models in `Shared/models/` and `Shared/dto/`.
- **Enums**: Standard system enums are defined in `Shared/enums/`.
- **TypeScript Generation**: TypeScript interfaces are generated automatically from Python Pydantic models by running `Scripts/generate_ts_interfaces.py`. No manual modifications are permitted to files in `Shared/generated/`.

## Folder Structure

```text
Shared/
├── contracts/        # Reusable interface schemas
├── dto/             # Request, Response, and WebSocket payloads
│   ├── __init__.py
│   ├── requests.py
│   └── responses.py
├── enums/           # System-wide enum states
│   └── __init__.py
├── generated/       # Automatically generated TypeScript type contracts
│   └── interfaces.ts
├── models/          # Domain-specific models
│   ├── __init__.py
│   ├── common.py
│   ├── market.py
│   ├── evidence.py
│   ├── recommendation.py
│   ├── portfolio.py
│   ├── research.py
│   ├── ai.py
│   └── notification.py
└── schemas/         # Centralized validation schemas
```

## Validation & Serialization Standards

- **Timestamps**: Timezone-aware UTC datetimes. Naive datetimes are strictly rejected.
- **Numbers**: Financial price and ratio calculations use `decimal.Decimal` on the backend to avoid floating-point errors. They serialize to numbers in JSON and map to `number` in TypeScript.
- **Volume/Quantity**: Quantities in positions and trades must be greater than zero. Volume in snapshots must be non-negative.
- **Ratios (Confidence/Weight)**: Values representing fractions must be strictly bounded between `0.0` and `1.0` (inclusive).

## TypeScript Generation Workflow

Whenever a Pydantic model is updated or added:
1. Update the appropriate Python file under `Shared/models/` or `Shared/dto/`.
2. Run the generator script:
   ```bash
   python Scripts/generate_ts_interfaces.py
   ```
3. Commit both the Python schema changes and the generated `Shared/generated/interfaces.ts` file.
