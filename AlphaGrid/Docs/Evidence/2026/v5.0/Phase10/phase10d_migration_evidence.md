---
Document ID: EVID-003
Title: "Phase 10d: Breakout Family Migration Evidence"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: Evidence
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-03
Dependencies: []
Referenced By: []
---

# Phase 10d: Breakout Family Migration Evidence

This document serves as the formal archival record of the Phase 10d execution. 

## 1. Environment Metadata
- **OS**: Windows 10
- **CPU**: Intel64 Family 6 Model 78 Stepping 3, GenuineIntel
- **RAM**: 8 GB
- **Python Version**: 3.11.9
- **NumPy Version**: 1.26.4
- **pandas Version**: 2.1.4

## 2. Discrepancy Reconciliation

### File Count Discrepancy (35 vs 26)
- The scratch repository (`AlphaGrid_Archived`) contained 35 files total.
- **26 files** were source code components (Features, Concepts, Methodologies, Signals, Strategies, Tests).
- **9 files** were temporary execution logs and scripts (e.g., `full_validation_output.txt`, `run_breakout_validation.py`, `diff_generator.py`). These were strictly excluded from the migration manifest to prevent polluting the production repository.

### Test Count Discrepancy (169 -> 184 -> 187)
- The baseline real repository contained 169 tests.
- During early scratch iterations, mock tests were added (reaching 184), but these included redundant logic.
- The final, approved Breakout test suite comprises exactly 18 tests (added across `test_breakout.py`, `test_features_math.py`, and `test_governance_breakout.py`).
- 169 (Baseline) + 18 (Breakout) = **187 final integration tests**.

## 3. Hash Verification Summary
A complete file-by-file verification was performed before and after the migration. 
- **Files Migrated**: 26
- **Files Merged**: 7
- **Result**: PASS (33/33 source vs destination SHA256 hashes successfully matched upon final execution).

Detailed hashes are embedded in the `migration_report.json` manifest below.

## 4. Rollback Evidence
The orchestrator's Hash Gate mechanism was independently triggered during execution:

- **Attempt 1 (Signals Module Import Error)**
  - *Failed:* ImportError during Stage F Regression.
  - *Rollback:* Triggered. All 33 files deleted or restored to backups.
  - *Result:* PASS (Repository hash matches original baseline).
- **Attempt 2 (Features Module Import Error)**
  - *Failed:* ImportError during Stage F Regression.
  - *Rollback:* Triggered. All 33 files deleted or restored to backups.
  - *Result:* PASS (Repository hash matches original baseline).
- **Attempt 3**
  - *Success:* All stages passed. Rollback not triggered.

## 5. Performance Benchmark
Basic boot metrics were recorded post-migration to ensure no severe latency regressions:
- **Import Latency**: ~30ms
- **Startup (Registry) Latency**: ~5ms
- **Total Boot Latency**: ~35ms
- **Resident Memory (RSS)**: ~32 MB

Raw output is available in `phase10d_benchmark.txt`.

## 6. Test Evidence Summary
- **Collected**: 187
- **Passed**: 187
- **Failed**: 0
- **Skipped**: 0
- **Xfailed**: 0
- **Duration**: 23.93 seconds
- **Warning Count**: 1 (pandas deprecation warning in dependency)

## 7. Evidence Manifest & Integrity Hashes
The raw execution artifacts have been snapshotted. To prevent accidental or malicious tampering of the evidence itself, the SHA-256 hashes of the evidence files are permanently recorded below:

| Artifact | SHA-256 Hash |
| :--- | :--- |
| `migration_report.json` | E5C4AD45E1D8C9122EF72FA072FF659912EAE80006F2FFC88C21E500DF6110EE |
| `phase10d_pytest_regression.txt` | 5E1C6C9FC18E7F57BEB351C476B1FB253F06955405D5D82AEBB099C43214A4C8 |
| `phase10d_benchmark.txt` | 2A0B3A44D44D84F35DD5198217B5677E94E815B667AAB0C6CB1E019A516D5393 |

## 8. Conclusion
**Phase 10d satisfies the governance criteria for Verified, contingent upon the referenced evidence artifacts (`migration_report.json`, regression logs, and benchmark reports) remaining available, unmodified, and traceable to the repository state documented in this report.**
