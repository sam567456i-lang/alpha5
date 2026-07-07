# Platform Boundary Report
## Violations
- `imbalance_engine.py` directly mutating state inside `swing_engine.py`. (Action: Enforce read-only DTOs).