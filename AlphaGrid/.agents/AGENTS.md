# AlphaGrid AGENTS.md (Enforcement Document)

> **NON-NEGOTIABLE REQUIREMENTS**
> This document defines the strict, non-negotiable enforcement safeguards for all agent activity in the AlphaGrid workspace. 

## 1. Repository Safeguards (Mandatory Before Write)
Before **every** write operation, you MUST print and verify:
1. Repository root
2. Active workspace
3. Current working directory
4. Git root (or explicitly state "not a Git repository")
5. Branch
6. Commit (or unavailable)
7. Target file
8. Existing file exists? (Yes/No)
9. Operation type (Add / Merge / Replace)
10. Backup created? (Yes/No)

If the target path is outside `C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid`, abort immediately.

## 2. Workspace Rules
- Always work against the user's local project as the single source of truth.
- Do not rely on Git history, previous conversations, or assumed intended designs over the local codebase.
- The repository behavior is determined only by the current local code executing successfully.
- Do not assume previous runtime blockers remain unresolved. Rediscover the current repository state from the code.

## 3. Write Protection & Anti-Simulation Rules
- **No Simulated Evidence**: Never generate simulated backtests, estimated runtimes, fabricated fingerprints, invented statistics, inferred PASS reports, or hypothetical coverage.
- **No Placeholders**: Never leave TODOs, FIXME comments, placeholder methods, dummy providers, fake services, or mock execution. Every write must be production-ready code.
- **No Fast-Fail Hacks**: Never introduce a fail-fast exception, synthetic dependency, or workaround solely to advance execution. Every piece of production code must be justified by an actual runtime failure.

## 4. Mandatory Execution Gates
- **Continuous Runtime Recovery**: Resume from the last verified runtime state; do not blindly restart.
- **First Failure Rule**: Stop immediately at the first runtime failure. Never patch multiple failures in one iteration. Fix only the first blocker, then execute again.
- **Execution Policy**:
  1. Execute the real repository.
  2. Use the canonical production entry point.
  3. Stop immediately at the first failure.
  4. Fix ONLY that blocker.
  5. Restart execution. Repeat.

## 5. Required Governance Documents
You must strictly abide by the rules defined in the following separated documents:
1. **`architecture_bible.md`**: Architecture, Layer rules, DTO contracts, Dependency rules.
2. **`Docs/master_ai_coding_constitution.md`**: Coding rules, Testing rules, Evidence rules, Review rules.
3. **`Docs/master_implementation_constitution.md`**: Migration, Rollback, Release, Freeze policies.

## 6. Canonical Repository Rule

The ONLY canonical project root is:

C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid

All project assets—including source code, documentation, registries, roadmaps, governance documents, evidence, ADRs, RFCs, templates, scripts, and tests—must be created, modified, and stored directly inside this repository.

Do NOT create or maintain project copies in:
- C:\Users\praka\.gemini\
- C:\Users\praka\.gemini\antigravity\
- C:\Users\praka\.gemini\antigravity\brain\
- C:\Users\praka\.gemini\antigravity\scratch\
- Any other temporary workspace.

If the active workspace is not the canonical repository, STOP and request that the correct repository be opened before making any project changes.

There must be exactly ONE source of truth.

## 7. Strict Architectural Governance

**Architecture Decision Record (ADR) Policy:**
- No new architectural layer may be introduced without an approved Architecture Decision Record demonstrating why existing layers cannot satisfy the requirement.
- The repository infrastructure is now feature-complete. Future work must deliver trading capabilities, not additional architectural layers.

**Dependency Hierarchy Constraint:**
The canonical dependency graph for all components must strictly flow downwards as follows:
`Market Data -> Math Core -> Indicator Engine -> Feature Generators -> Concepts -> Methodologies -> Signals -> Strategies`
Strategies must never instantiate indicators directly. Strategies rely purely on semantic building blocks (concepts, methodologies, signals).

**Capability Completion Rule:**
No new capability reaches "Complete" until it satisfies all 7 mandatory gates:
`Capability -> Registry -> Implementation -> Validation -> Documentation -> Benchmark -> Evidence -> Freeze`
Partially implemented features without validation, documentation, and evidence are forbidden.
