---
Document ID: GOV-001
Title: "AI Agent Governance"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: Governance
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-03
Dependencies: []
Referenced By: []
---

# AI Agent Governance

## 1. Purpose
Defines the strict operational boundaries for autonomous AI coding agents interacting with the AlphaGrid repository. This complements `.agents/AGENTS.md`.

## 2. Allowed Autonomy
- AI agents are allowed to autonomously plan, implement, and validate code within a defined subsystem.
- AI agents are **NOT** allowed to unilaterally change frozen architecture, skip review gates, or override the Policy Engine.

## 3. Evidence Requirements
AI generated code must be accompanied by mathematically verifiable Evidence IDs. "Passing" tests is insufficient without cryptographic proof of execution.

## 4. Human Approval Boundaries
- Major architecture changes (RFCs).
- Changes to cross-family registries.
- Relaxing of risk or capital limits.
- Bumping MAJOR versions.

## 5. Self-Verification & Rollback
AI agents must verify their own work using the defined static analysis and testing tools before presenting it to the user. If a test fails, the agent must either self-heal or rollback the workspace to the prior clean state.
