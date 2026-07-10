---
Authority: Level 2
Parent: Docs/Governance/Platform10_Family_Development_Standard.md
Type: Capability Family Specification
Domain: Primitives
Platform: 10
Version: 1.0.0
Status: ACTIVE
CRL: CRL-2

# Swing Family Specification

**Family:** Swing
**Owns:** ✓ Object, ✓ Lifecycle, ✓ Quality
**Consumes:** ✓ Price, ✓ Statistics, ✓ Time
**Publishes:** ✓ SwingEvidence, ✓ PivotLifecycleEvidence, ✓ SwingQualityEvidence
**Never Publishes:** ✗ Events, ✗ Methodology Terms, ✗ Ranges, ✗ Trendlines

## 1. Scope Definition
The **Swing Family** bridges the gap between raw statistical data and higher-order market structure. It strictly owns objective pivot extraction, geometric swing relationships, and multi-scale hierarchy mapping. 

It explicitly **does not** compute BOS (Break of Structure), sweeps, or other structurally semantic behaviors (Rule 5).

## 2. Engine Components
The family is composed of the following six orchestrated engines:

### 2.1 Pivot Engine
- **Purpose:** Extracts turning points based on pluggable, objective criteria (e.g., N-bar fractal, ZigZag).
- **Inputs:** `PriceEvidence`, `StatisticsEvidence` (for adaptive models).
- **Outputs:** `PivotHigh`, `PivotLow`.

### 2.2 Persistence Engine
- **Purpose:** Manages the strict sequential lifecycle of every detected pivot to prevent downstream families from consuming incomplete data.
- **Inputs:** Raw Pivots from `PivotEngine`.
- **Outputs:** Lifecycle State (`Candidate` → `Developing` → `Confirmed` → `Active` → `Invalidated` → `Archived`).

### 2.3 Classification Engine
- **Purpose:** Categorizes a confirmed swing's nominal type within a given fractal scale.
- **Inputs:** Confirmed Pivots.
- **Outputs:** `Major`, `Intermediate`, `Minor`.

### 2.4 Relationship Engine
- **Purpose:** Mathematically compares adjacent pivots to determine objective positioning.
- **Inputs:** Classified Pivots.
- **Outputs:** 
  - `Higher High (HH)`, `Higher Low (HL)`, `Lower High (LH)`, `Lower Low (LL)`
  - `Equal High (EQH)`, `Equal Low (EQL)`
  - `Near Equal High`, `Near Equal Low`, `Higher Equal`, `Lower Equal`

### 2.5 Hierarchy Engine
- **Purpose:** Maps swings into recursive multi-scale trees rather than rigid tiers. (e.g., a primary swing contains secondary swings, which contain minor swings).
- **Inputs:** Swing Relationships, Classification.
- **Outputs:** `SwingTreeEvidence`.

### 2.6 Quality Engine
- **Purpose:** Quantifies the objective significance of a swing without methodology interpretations.
- **Inputs:** `SwingEvidence`, `StatisticsEvidence`, `PriceEvidence` (Volume).
- **Outputs:** 
  - `Magnitude`
  - `Duration`
  - `Symmetry`
  - `Volatility-adjusted significance`
  - `Confirmation bars`

## 3. Certification Gates
This family cannot be marked complete until all engines pass the strict 19-step standard execution lifecycle, culminating in a `Swing_Certification.md` report.
