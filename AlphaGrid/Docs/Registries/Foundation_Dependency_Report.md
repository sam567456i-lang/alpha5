---
Authority: Level 1
Parent: Docs/Governance/Constitution.md
Children: None
Supersedes: None
Version: 1.0.0
Status: ACTIVE
---

# Foundation Dependency Report

This report tracks the specific failure impacts and recovery paths for the foundational infrastructure supporting AlphaGrid.

## Replay Engine
- **Depends On:** Configuration Registry, Event Bus, Snapshot Manager
- **Used By:** Platform 10, Platform 11, Platform 12, Validation Services
- **Initialization Order:** 4
- **Failure Impact:** Critical (Entire pipeline halts, determinism lost)
- **Recovery Strategy:** Reload from last valid Snapshot + Event Journal Replay

## Global Registry
- **Depends On:** BaseRegistry implementations
- **Used By:** All Platforms, All Programs
- **Initialization Order:** 1
- **Failure Impact:** Fatal (System cannot boot or resolve any dependencies)
- **Recovery Strategy:** Hard restart. Validated by `registry_boot_validator`.

## Capability Knowledge Graph
- **Depends On:** Global Registry
- **Used By:** Platform 12, AI Platform, Conformance Validators, Planners
- **Initialization Order:** 2
- **Failure Impact:** High (System boots, but dynamic routing and validations fail)
- **Recovery Strategy:** Recompile from Global Registry manifest.

## Configuration Loader
- **Depends On:** File System / Network Config Store
- **Used By:** Configuration Registry
- **Initialization Order:** 0 (Absolute First)
- **Failure Impact:** Fatal (Boot sequences fail)
- **Recovery Strategy:** Fallback to `default.yaml` cached state.

## Event Bus
- **Depends On:** Configuration
- **Used By:** All Platforms
- **Initialization Order:** 3
- **Failure Impact:** Fatal (No messages pass between components)
- **Recovery Strategy:** Reboot bus; replay missed events from Journal.
