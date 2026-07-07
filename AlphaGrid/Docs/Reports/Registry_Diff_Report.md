# Registry Diff Report

> **DIFF APPROVAL GATE**: This document represents the planned modifications. The live repository has NOT been altered.

## 1. Artifacts to be Created
- `Docs/Governance/taxonomy.yaml` (Containing complete hierarchical trees for Liquidity, Market Structure, Wyckoff, Order Flow, etc.)
- `Docs/Governance/methodology_registry.yaml` (Migrating ICT, SMC, Wyckoff, ORB, etc.)
- `Docs/Governance/Capability_Matrix.md` (Master planning matrix for supported markets/styles/timeframes)

## 2. Schema Expansion on master_capability_registry.yaml
Every entry will have its schema extended backward-compatibly:
```diff
+ entity_type: capability # (or platform, family, service, infrastructure)
+ lifecycle_status: Placeholder
+ supported_markets: []
+ supported_styles: []
+ supported_timeframes: []
+ required_data: []
+ required_states: []
+ planned_dependencies: [Raw Price Data] # Shifted from dependencies
- consumes: [Raw Price Data] # Cleared for placeholders
```

## 3. Taxonomy Injection & Hierarchical IDs
Over 150 unique capabilities will be generated with strict naming:
- `[+] liq.obj.time.pdh` (Previous Day High)
- `[+] liq.event.sweep` (Liquidity Sweep)
- `[+] liq.fp.fvg` (Fair Value Gap)
- `[+] ms.bos` (Break of Structure)
- `[+] auction.poc` (Point of Control)
- `[+] wy.spring` (Wyckoff Spring)
- `[+] vol.delta` (Volume Delta)
- `[+] crypto.funding_rate` (Funding Rate Placeholder)
- `[+] forex.dxy` (DXY Placeholder)
*(Full list corresponds exactly to the 17 taxonomy domains requested)*

## 4. Services Registration
- `[+] svc.orchestrator` (Capability Orchestrator)
- `[+] svc.confidence_engine`
- `[+] svc.evidence_engine`
- `[+] infra.dashboard`

## 5. Root Versioning Metadata
The root yaml will be wrapped with 10 explicit fields:
`registry_version`, `schema_version`, `taxonomy_version`, `architecture_version`, `project_os_version`, `migration_version`, `generator_version`, `audit_timestamp`, `generated_by`, `change_id`.
