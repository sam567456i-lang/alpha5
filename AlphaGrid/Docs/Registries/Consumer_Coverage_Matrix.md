---
Authority: Level 1
Parent: Docs/Governance/Constitution.md
Children: None
Supersedes: None
Version: 1.0.0
Status: ACTIVE
---

# Consumer Coverage Matrix

This document enforces a strict architectural rule: **If a capability has no downstream consumer, it must not be built.**

Every capability in the system must map to at least one active consumer profile, policy, or platform.

| Capability (Family/Engine) | Primary Consumers | Secondary Consumers | Status |
|---|---|---|---|
| **Order Block Engine** | Platform 11 (ICT, SMC), Platform 12 | Platform 14, Dashboard | CRL-7 (Certified) |
| **Volume Climax Engine** | Platform 11 (Wyckoff), Platform 12 | Dashboard | CRL-2 (Specification) |
| **Footprint Extractor** | Platform 12 (Decision) | Analytics | CRL-0 (Concept) |
| **BOS/CHOCH Engine** | Platform 11 (ICT, SMC) | Platform 14, Dashboard | CRL-7 (Certified) |
| **Multi-Timeframe Engine** | Platform 12 (Conflict Res) | Analytics | CRL-1 (Architecture) |
