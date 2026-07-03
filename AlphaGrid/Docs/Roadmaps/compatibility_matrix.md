---
Document ID: ROAD-003
Title: "Compatibility Matrix"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: Roadmaps
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-03
Dependencies: []
Referenced By: []
---

# Compatibility Matrix

## 1. Purpose
Defines the supported version combinations of the core AlphaGrid architectural layers to prevent runtime incompatibilities.

## 2. Platform Support Matrix

| Architecture Version | DTO Schema Version | Registry Schema Version | Configuration Schema Version | Runtime Framework |
| :--- | :--- | :--- | :--- | :--- |
| **5.1.x** (Current) | 3.x.x | 4.x.x | 2.x.x | Phase 10 |
| **5.0.x** (Legacy) | 2.x.x | 3.x.x | 2.x.x | Phase 9 |
| **4.x.x** (Archived) | 1.x.x | 2.x.x | 1.x.x | Phase 8 |

*Note: Mixing versions outside these row bounds is formally unsupported and blocked by the Runtime Framework's version compatibility checks.*
