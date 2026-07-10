---
Authority: Level 1
Parent: Constitution.md
Children: None
Supersedes: None
Version: 1.0.0
Status: ACTIVE
---

# Document Hierarchy

To eliminate ambiguity, every document in the AlphaGrid ecosystem must declare its authority level. A lower-level document may **never** contradict a higher-level document.

## Authority Levels

### Level 0: Constitution
- **Contents:** Principles, boundaries, determinism rules.
- **Authority:** Supreme. Never discusses implementation details.
- **Examples:** `Constitution.md`

### Level 1: Architecture Specifications
- **Contents:** The Master Roadmap and End-to-End flows.
- **Authority:** Defines *what* exists and *how* data flows globally.
- **Examples:** `AlphaGrid_Master_Roadmap.md`, `AlphaGrid_End_to_End_Architecture.md`

### Level 2: Platform Specifications
- **Contents:** Detailed designs for Platforms 10 through 15.
- **Authority:** Defines internal Platform logic, SDKs, and Extension Policies.
- **Examples:** `Platform10.md`, `Platform11.md`

### Level 3: Program Specifications
- **Contents:** Detailed designs for Auxiliary Programs (A-K).
- **Authority:** Defines non-deterministic systems like Knowledge, AI, and Operations.
- **Examples:** `Knowledge_Platform.md`, `Research_Platform.md`

### Level 4: Implementation Plans
- **Contents:** Temporary task lists and execution strategies for building components.
- **Authority:** Ephemeral. Valid only during active development waves.
- **Examples:** `implementation_plan.md`, `task.md`

### Level 5: ADRs (Architecture Decision Records)
- **Contents:** Point-in-time decisions explaining *why* a specific architecture was chosen.
- **Authority:** Permanent record, but superseded by Level 1/2 updates.
- **Examples:** `ADR-007_Universal_Zone_Framework.md`

### Level 6: Developer Guides
- **Contents:** How-to guides, scaffolding instructions, environment setup.
- **Authority:** Instructional.
- **Examples:** `Zone_Developer_Guide.md`

### Level 7: Reference Material
- **Contents:** External papers, dictionaries, glossaries, logs.
- **Authority:** Informational only.
- **Examples:** `glossary.md`, `decision_log.md`

## Mandatory Frontmatter
Every markdown file in `Docs/` MUST include the following YAML frontmatter:
```yaml
---
Authority: Level X
Parent: [Parent Document]
Children: [Child Documents or None]
Supersedes: [Legacy documents replaced by this one]
Version: x.x.x
Status: [DRAFT | ACTIVE | FROZEN | DEPRECATED]
---
```
