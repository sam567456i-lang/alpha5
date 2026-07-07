
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
