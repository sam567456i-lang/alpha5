---
Authority: Level 1
Parent: Docs/Governance/Constitution.md
Children: None
Supersedes: None
Version: 1.0.0
Status: ACTIVE
---

# Architecture Review Checklist

Every Pull Request that introduces a new capability, modifies an SDK contract, or adds a new dependency MUST include this checklist in the PR description. If any answer violates the Constitution, the PR must be closed.

## The Checklist

1. **Which Domain owns this?** (e.g., Market, Execution)
2. **Which Platform owns this?** (e.g., Platform 10, Platform 12)
3. **Which Program owns this?** (e.g., Trading Core, Knowledge Platform)
4. **Is an ADR required?** (Yes/No) If Yes, link the ADR.
5. **Does it preserve replayability?** (Yes/No) Ensure no references to live system clocks or external state mutation.
6. **Does it preserve provenance?** (Yes/No) Ensure evidence identities are properly linked downstream.
7. **Does it preserve determinism?** (Yes/No) Ensure identical inputs produce mathematically identical outputs.
8. **Does it introduce cross-layer coupling?** (Yes/No) Ensure it does not bypass the SDK interfaces (e.g., P15 reading P10 memory).
9. **Is it independently testable?** (Yes/No)
10. **Does it duplicate an existing capability?** (Yes/No)
11. **Does it change a public contract?** (Yes/No)
12. **Does it require migration?** (Yes/No)
