---
Authority: Level 1
Parent: Docs/Governance/Constitution.md
Children: None
Supersedes: None
Version: 1.0.0
Status: ACTIVE
---

# Registry Hierarchy

This document maps the structural hierarchy of ownership and categorization within the AlphaGrid ecosystem. It ensures that every single piece of logic has an exact, singular place where it belongs.

## 1. Global Registry Model

All previous fragmented registries are superseded by this single hierarchical tree:

```text
Global Registry
├── Domain Registry (e.g., Market, Execution, Risk)
├── Platform Registry (e.g., P10, P11, P12)
├── Program Registry (e.g., AI Platform, Operations)
├── Capability Registry (The master inventory)
├── Feature Registry (Specific AI or Decision features)
├── Evidence Registry (P10 output types)
├── Interpretation Registry (P11 output types)
├── Decision Registry (P12 output types)
├── Plugin Registry (External integrations)
├── Profile Registry (Methodologies)
├── Policy Registry (Configurable thresholds)
├── SDK Registry (Public contracts)
├── Artifact Registry (Builds and binaries)
├── Knowledge Registry (Concepts and ontology)
├── Experiment Registry (Research platform runs)
├── Model Registry (ML/RL weights)
└── Repository Registry (External dependencies)
```

## 2. Master Ownership Taxonomy

Every unit of work in the trading pipeline descends through this exact ownership tree:

`Domain -> Capability Family -> Engine -> Rule -> Evidence`

**Example:**
- **Domain:** Market Structure Domain
- **Family:** Structure Family
- **Engine:** `SwingEngine`
- **Rule:** `SwingHighRule`
- **Evidence Output:** `SwingEvidence`

If a new PR cannot perfectly map its feature into this taxonomy, it indicates architectural drift and the PR must be rejected or redesigned.
