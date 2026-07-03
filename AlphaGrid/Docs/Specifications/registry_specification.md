---
Document ID: SPEC-004
Title: "Registry Specification"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: Specifications
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-03
Dependencies: []
Referenced By: []
---

# Registry Specification

## 1. Overview
Defines the strict schema for the `master_capability_registry.yaml` file, which serves as the static dependency injection graph for the platform.

## 2. Interfaces
- `IRegistryParser`
- `IRegistryValidator`

## 3. DTOs
- `CapabilityDefinitionDTO`

## 4. Schemas
The YAML schema must include:
- `id` (unique capability identifier)
- `type` (Feature, Concept, Methodology, Strategy, etc.)
- `version`
- `dependencies` (explicit list of required IDs)
- `parameters` (default configurations)

## 5. Examples
```yaml
capabilities:
  - id: "feat-rsi-v1"
    type: "Feature"
    version: "1.0.0"
    dependencies: ["data-close-price"]
```

## 6. Compatibility
- Removing a capability from the registry is a breaking change.

## 7. Versioning
- Changing the schema of the YAML file itself is a MAJOR bump.

## 8. Migration
- Automated migration scripts must be provided for schema changes.

## 9. References
- Registry Engine Phase.
