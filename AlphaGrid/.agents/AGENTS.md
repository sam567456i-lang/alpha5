# AlphaGrid Permanent Governance Directive

## Mandatory Architecture Continuity, Change Management, and Pre-Phase Validation

### Purpose
This directive is permanently active for the AlphaGrid repository. Its objective is to ensure that **no architectural decision, capability, requirement, dependency, governance rule, roadmap update, implementation detail, or design discussion is ever forgotten, silently replaced, duplicated, or bypassed** during development.

---

# Rule 1 — Architecture Is the Source of Truth
Before performing **any implementation**, the repository must be considered the current source of truth. No implementation may rely only on recent conversation context. The entire architecture must always be reconstructed from repository documentation before work begins.

# Rule 2 — Mandatory Pre-Phase Repository Review
Before starting **every platform**, **every phase**, **every methodology wave**, **every plugin**, **every refactor**, **every audit**, or **every implementation**, the AI must perform a mandatory repository review of all core Governance, Project Bible, Roadmap, and Registry documents. Implementation is forbidden until this review is complete.

# Rule 3 — Continuous Architecture Memory
Every architectural change must be permanently recorded. Nothing may exist only in conversation. Every decision must become repository knowledge.

# Rule 4 — Architecture Change Log
Maintain a permanent architecture history in `Docs/Governance/Architecture_Change_Log.md`. Nothing changes without an entry containing Date, Decision ID, Summary, Reason, Evidence, Files affected, Risk assessment, and Approval status.

# Rule 5 — Repository Evolution Record
Every implementation updates the Repository Evolution Record, including new/modified/deprecated capabilities, DTOs, plugins, and phase completion.

# Rule 6 — Mandatory Impact Analysis
Before changing anything the AI must determine dependencies, what consumes/produces it, and what downstream platforms/tests change. If impact is unknown, implementation stops.

# Rule 7 — Duplicate Prevention
Before adding anything the AI must verify it doesn't partially/fully exist, have a different owner, or duplicate documentation.

# Rule 8 — Missing Capability Detection
Every implementation must compare the Current repository vs Canonical architecture. Any missing capability must be recorded.

# Rule 9 — Capability Ownership
Every capability must have exactly one owner. No capability may have multiple owners.

# Rule 10 — Mandatory Completion Checklist
Before every implementation complete the mandatory checklist (Architecture, Repository, Governance, Implementation, Validation, Completion).

# Rule 11 — No Forgotten Changes
Before every new task the AI must review the latest Architecture Change Log, Repository Evolution Record, Freeze, Phase Exit, Platform docs, and Registries.

# Rule 12 — End-to-End Validation
After every completed phase, the entire implemented pipeline must execute and be validated through regression testing.

# Rule 13 — Wave Validation
Every methodology wave follows strict progression from Planning through Implementation, Cross-Wave Regression, Documentation, and Freeze.

# Rule 14 — Architecture Drift Prevention
The AI must continuously compare Architecture, Documentation, Repository, Registries, DTOs, and Implementation. Any inconsistency must be reported immediately.

# Rule 15 — Never Forget Principle
At the beginning of every implementation the AI must assume: "I may have forgotten something." It must reconstruct repository knowledge by reviewing documentation before writing any code.

# Rule 16 — Project Completion Checklist
Maintain a living document `Docs/Governance/Master_Project_Completion_Checklist.md`. Every capability in AlphaGrid must appear exactly once.

# Rule 17 — Mandatory Audit Before Every Phase
Before beginning any new phase, ProjectOS must automatically execute all Integrity, Architecture, Duplicate Detection, and Evolution reviews.

# Final Principle
AlphaGrid evolves by **controlled extension**, never by forgotten conversations, undocumented decisions, duplicated capabilities, or silent architectural drift. Every decision is recorded. Every change is traceable. Every implementation is reviewed. Every phase begins with reconstruction of repository knowledge. Every phase ends with certification, documentation synchronization, and immutable history.

# Rule 18 — Foundation Preservation & Governance
This directive is mandatory for all future AlphaGrid development.

1. **Foundation Is Permanent**: The introduction of the Ontology, Registries, and Governance Layer does NOT replace or redesign the existing Foundation Layer (API, Database, Plugin SDK, Event Bus, etc.).
2. **Architecture Layering**:
   - Governance Layer (Ontology, Registries, Audit, Certification, Lifecycle)
   - Platform Layer (P0 - P22)
   - Foundation Layer (API, Database, Plugin SDK, Event Bus, DTOs, Replay, Testing)
3. **Plugin Framework**: The Plugin SDK remains the canonical implementation. Do not rewrite it. Only extend plugins with governance metadata (ontology_id, capability_id, version, lifecycle, certification_state, dependency_list).
4. **API Policy**: APIs expose platform capabilities but never implement business logic.
5. **Database Policy**: Existing database structures remain. Governance only enriches them (e.g. Audit History, Replay Runs).
6. **Event Bus Policy**: The Event Bus implementation remains unchanged. Governance only formalizes event definitions.
7. **Foundation Freeze**: The Foundation Layer is a governed subsystem. Modifications require an ADR, Regression Validation, and Human Approval.
8. **Universal Audit Structure**: The repository audit must permanently contain four independent sections: Foundation Audit, Platform Audit, Capability Audit, and Integration Audit. The Foundation Audit must independently score API, Database, Plugin SDK, DTO, Event Bus, Replay, DI, Logging, Config, and Caching.

