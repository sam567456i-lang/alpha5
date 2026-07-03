---
Document ID: DOC-031
Title: "Migration Notes"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: Phase_10B
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-03
Dependencies: []
Referenced By: []
---

# Migration Notes

Upstream datasets MUST be explicitly UTC localized. Naive timezones will now result in immediate pipeline failure (DataError).
