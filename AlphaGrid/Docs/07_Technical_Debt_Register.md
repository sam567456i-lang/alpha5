# Technical Debt Register

## Role
This register tracks all non-ideal implementations that bypass Project OS certification standards. Nothing discovered during repository audits may disappear silently.

## Tracked Debt Categories
All entries must belong to one of the following explicitly tracked categories:
- Legacy modules (Scheduled for deprecation)
- Archived code (Pending final deletion)
- Duplicate implementations (Violates DRY)
- Dead plugins (Unused capabilities)
- Deprecated DTOs
- Deprecated registries
- Broken dependencies
- TODOs / FIXME tags in codebase
- Disabled or skipped tests
- Compatibility shims
- Temporary workarounds (Hardcodes, magic numbers)

## Active Debt Entries

### 1. Python Environment Mismatch
- **Category**: Compatibility shim
- **Description**: Environment is Python 3.11.9, but `pyproject.toml` asserts `>= 3.12`.
- **Status**: OPEN
- **Action Required**: Re-align `pyproject.toml` or upgrade environment.

### 2. Geometry Cache Incomplete
- **Category**: TODO
- **Description**: Downstream concept engines currently expect a populated `GeometryCache`, but caching lifecycle is partially implemented.
- **Status**: OPEN
- **Action Required**: Finalize Phase 10C cache object definitions.
