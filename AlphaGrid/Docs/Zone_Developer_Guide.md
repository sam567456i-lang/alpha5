# Zone Developer Guide

The AlphaGrid spatial architecture uses a strict composition-based framework. Subclassing is entirely prohibited. To add a new zone classification, follow this exact workflow:

### Step 1: Register Capability
Define your abstract methodology capability in `Docs/Governance/registry/capability_registry.yaml`. This ensures the capability is properly tracked inside the universal governance framework.

### Step 2: Register Zone Properties
Map the physical spatial constraints and behavioral policies into `Docs/Governance/registry/zone_registry.yaml`. Ensure you define strict performance budgets (`max_latency_ms`), required metadata inputs (`GeometryDTO`, `StructureDTO`), and spatial topologies.

### Step 3: Register Zone Lifecycle
Define the specific transition triggers for PENDING, ACTIVE, and MITIGATED states inside `Docs/Governance/registry/zone_state_machine_registry.yaml`.

### Step 4: Map Capability
Bridge the abstract capability to the spatial zone topology inside `Docs/Governance/registry/zone_capability_registry.yaml`.

### Step 5: Orchestrate Detector
Create a lightweight Python implementation inheriting purely from `ZoneDetectorBase` in `Backend/platforms/platform8_analysis/detectors/`. **Do not write math logic in the detector.** Only invoke the pre-built spatial index tools and generic engines (e.g., `OverlapEngine`).

### Step 6: Certify & Freeze
Run the central certification checks:
```bash
python ProjectOS/audits/zone_registry_certification.py
```
If your registry configuration emits a `Zone Registry Certified` pass, you are ready to freeze.
