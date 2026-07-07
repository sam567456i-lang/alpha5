# Registry Drift Report

## Architecture vs Registry Drift
- **Taxonomy Drift**: DETECTED. The Architecture Bible contains institutional taxonomies (Wyckoff, Volume, AMT) that are absent or flattened in the master registry.
- **Dependency Drift**: DETECTED. Placeholders contain hardcoded implementation dependencies (`consumes`/`produces`) rather than `planned_dependencies`.
- **Methodology Drift**: DETECTED. Methodologies are stored as capabilities.
