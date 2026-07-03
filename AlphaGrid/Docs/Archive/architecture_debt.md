---
Document ID: ARCHV-001
Title: "Architecture Debt Ledger"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: Archive
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-03
Dependencies: []
Referenced By: []
---

# Architecture Debt Ledger

This document tracks known architectural compromises or limitations that are intentionally bypassed to adhere to the Institutional Recovery Protocol (One Phase = One Blocker).

## AD-004: DI-Aware Plugin Constructors
- **Description**: The current plugin loader in `registry_hook.py` assumes zero-argument constructors for plugins. Repository evidence proves multiple production plugins (e.g., `BreakoutConceptGenerator`, `StrengthConceptGenerator`) require injected configuration (`source`, `config`) during instantiation.
- **Recovery Impact**: None. The pipeline naturally advanced using the plugins that loaded successfully.
- **Architecture Impact**: High. Many intended concepts are currently bypassed and unavailable.
- **Resolution**: Future phases must introduce DI-aware plugin construction, allowing plugins to request dependencies via their constructors or a standard factory interface.
