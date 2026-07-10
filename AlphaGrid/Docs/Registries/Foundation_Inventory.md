---
Authority: Level 1
Parent: Docs/Governance/Constitution.md
Children: None
Supersedes: None
Version: 1.0.0
Status: ACTIVE
---

# Foundation Inventory

This document is the operational catalog for all Phase 0 foundational services. 
If a service is listed here, it exists; do not rebuild it.

| Service | Domain | Owner | Consumers | CRL | Status | Frozen | ADR | Tests |
|---|---|---|---|---|---|---|---|---|
| **Global Registry** | Foundation | Core Team | All Platforms | CRL-4 | Implemented | No | ADR-040 | `test_foundation.py` |
| **Capability Graph** | Foundation | Core Team | P10, P11, AI | CRL-4 | Implemented | No | ADR-041 | `test_foundation.py` |
| **Replay Engine** | Simulation | Core Team | P10, P11, P12 | CRL-5 | Verified | Yes | ADR-022 | `test_foundation.py` |
| **Config Loader** | Operations | DevOps | All Platforms | CRL-5 | Verified | Yes | ADR-015 | `test_foundation.py` |
| **Snapshot Manager**| Operations | DevOps | Operations | CRL-5 | Verified | Yes | ADR-018 | `test_foundation.py` |
| **Event Bus** | Execution | Core Team | All Platforms | CRL-5 | Verified | Yes | ADR-011 | `test_foundation.py` |
| **Scheduler** | Execution | Core Team | P10, P13 | CRL-5 | Verified | No | ADR-012 | `test_foundation.py` |
| **Telemetry** | Observability| DevOps | P15, Dashboard | CRL-4 | Implemented | No | ADR-028 | `test_foundation.py` |
