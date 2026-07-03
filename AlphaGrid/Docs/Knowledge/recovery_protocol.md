---
Document ID: KNOW-006
Title: "Institutional Recovery Protocol"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: Knowledge
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-03
Dependencies: []
Referenced By: []
---

# Institutional Recovery Protocol

This document defines the strict, machine-enforced governance rules for developing and recovering the AlphaGrid platform.

## 1. Mandatory Recovery Gate Checklist
Every phase must sequentially complete the Production Acceptance Gate. If any step fails, the phase is not complete.
1. Repository investigation completed.
2. Architecture Bible & ADRs reviewed.
3. Contracts and Dependencies verified.
4. Integration matrix completed.
5. Implementation strictly targets the current blocker only.
6. Real production code implemented (no mocks).
7. Canonical pipeline executed (`python -m scratch.run_canonical`).
8. Real dataset executed.
9. Data lineage verified.
10. Output consumed by the downstream layer.
11. First downstream boundary (blocker) reached.
12. Manifest generated.
13. Evidence frozen.
14. Cursor updated.

## 2. Recovery Cursor
Every artifact should end with a "Recovery Cursor" tracking the exact verified state:
`Current Layer`, `Previous Verified Layer`, `Verified Pipeline` (the entire chain of passed components), `Current Blocker`, `Next Target`, `Resume Command`.

## 3. Automatic Recovery Resume
If recovery leaves the current blocker for investigation, ADR work, or debugging, it must **automatically return to the last unresolved runtime blocker**, complete it, rerun the canonical pipeline, and only then advance.

## 4. Recovery Lock
Once a blocker is active, **no code outside the dependency chain may be modified.** (e.g., If the blocker is `PrimitiveSignals`, modifying `Dashboard` is forbidden unless required by dependency analysis). This prevents scope creep.

## 5. Strategy Promotion Lifecycle (Research Governance Rule)
The architecture explicitly defines the promotion path for strategies, concepts, features, evidence models, and AI models:
`Idea -> Experimental -> Research -> Candidate -> Shadow -> Production -> Watch -> Degraded -> Retired`

**CRITICAL RULE:** No strategy, methodology, concept, feature, evidence model, or AI model may be promoted unless it has strictly passed the **Scientific Validation program** and the **Production Acceptance Gate**. Nothing bypasses this. No manual override, and no AI shortcut.

## 6. Proof Before Claim Rule
A phase may not claim: `PASS`, `VERIFIED`, `COMPLETE`, or `RESOLVED` unless there exists machine-generated evidence from the canonical pipeline supporting the claim. Narrative summaries do not count as evidence.

## 7. Continuous Pipeline Growth Rule
The canonical pipeline grows cumulatively. Every new phase extends the existing production pipeline rather than creating a new execution path. Previously verified stages must execute again in every subsequent phase, using the real output of each upstream stage as the input to the next stage. The pipeline is never reset, forked, bypassed, or partially executed for verification.
