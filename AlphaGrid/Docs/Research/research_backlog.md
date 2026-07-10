# AlphaGrid Research Backlog

The era of architectural roadmaps and framework milestones is over. Success is no longer measured by frameworks completed, but by **hypotheses tested and falsified**. 

The goal of this backlog is to push rules through empirical validation as rapidly and rigorously as possible. Rejecting bad ideas is progress.

## Current Queue
| Priority | Task | Goal | Exit Criteria | Status |
| :--- | :--- | :--- | :--- | :--- |
| **P1A** | **Engineering Dataset** | Generate and certify `ENG-SYN-0001`. | Dataset generated, hashed, and certification report produced. | `COMPLETED` |
| **P1B** | **Engineering Pipeline** | Verify ingestion, replay, hashing, and labeling operate correctly. | Synthetic end-to-end run completes without errors. | `COMPLETED` |
| **P1C** | **First Research Dataset** | Import real BTCUSDT 1H history, produce `WF-BTCUSDT-2024Q1-v1`. | Dataset frozen, hashed, and marked Research Ready. | `COMPLETED` |
| **P1D** | **Cross-Market Datasets** | Expand to NIFTY and Indian Equities to satisfy promotion requirements. | Multiple datasets hashed and registered. | `NOT STARTED` |
| **P2** | **Label Validation** | Generate objective labels, run drift validation, freeze, and register. | `LabelSet v1` frozen and checksum recorded. | `COMPLETED` |
| **P3a** | **Detection Quality** | Execute `EXP-000001` to measure empirical Precision, Recall, and F1. | Experiment completed with machine-generated report. | `COMPLETED` |
| **P3b** | **Stability** | Execute `EXP-000001` across market regimes. | Machine-generated stability report produced. | `PARTIAL` |
| **P4A** | **Experiment Report** | Produce formal report on observed failures and hypotheses. | Human-readable report committed. | `PARTIAL` |
| **P4B** | **Research Review** | Determine if failure was caused by: Rule, Labels, Dataset, Config, or Design. | Report reviewed and root cause categorized. | `COMPLETED` |
| **P5** | **Decision** | Promote, Revise, Reject, Archive, or Needs More Data. | Decision: Isolate H1 and H2 into EXP-000002/000003. | `COMPLETED` |
| **P6** | **Next Research Cycle** | Execute EXP-000002/3 factorial isolation. | Factorial execution completed. | `COMPLETED` |
| **P7** | **Objective Structure Expansion** | Expand the measurement vocabulary available to research (e.g. SwingCluster, TouchFrequency). | New data primitives scheduled for implementation. | `NEXT` |

---

## The Immutable Research Sequence
To prevent unconscious curve-fitting during execution, every experiment must strictly follow this physical sequence:
1. Freeze Dataset
2. Freeze Labels
3. Freeze Rule Version
4. Freeze Configuration (e.g., `CFG-0001`). *Configurations are permanently immutable. Changing a single parameter requires `CFG-0002`.*
5. Run Experiment
6. Analyze Results
7. Decide: Promote, Revise, Reject, Archive, or Needs More Data
*(Only then may code be altered).*

---

## Cross-Market Promotion Policy
To prevent curve-fitting to a single environment (e.g. Crypto), achieving `Production` status strictly requires mathematical robustness. The minimum requirements are:
- At least **3 independent datasets**
- At least **2 market types** (e.g., Crypto, Index, Equities)
- At least **3 market regimes** (e.g., Trending, Ranging, High Volatility)
- At least **2 timeframes**

*Cross-Market Reporting is mandatory for all experiments.*

---

## Prohibited Infrastructure
Unless a real empirical experiment explicitly demands it, the following activities are strictly prohibited:
- New platform definitions
- New architectural constitutions
- New framework layers
- New registries
- New SDKs
- New lifecycle states

*The existing infrastructure is sufficient. Let empirical work drive further engineering, not the other way around.*

---

## Research Debt
Every experiment will inevitably spawn questions that must be postponed to prevent derailment. They are recorded here.

- **RD-001**: Investigate adaptive ATR thresholds vs static standard deviations.
- **RD-002**: Evaluate volume-confirmed liquidity sweeps (Level II depth integration).
- **RD-003**: Test alternative swing validation definitions (e.g., fractional pivots).

---

## The First Major Milestone
The first research milestone is a reproducible sequence of experiments that results in at least one promoted hypothesis and several justified rejections, looking something like this:

| Experiment | Result |
| :--- | :--- |
| `EXP-000001` | Rejected |
| `EXP-000002` | Revised |
| `EXP-000003` | Rejected |
| `EXP-000004` | Promoted |
| `EXP-000005` | Rejected |

*A lab that only produces "successful" experiments is suffering from confirmation bias. The value of AlphaGrid is determined by the quality, reproducibility, and honesty of the research recorded in the experiment ledger.*
