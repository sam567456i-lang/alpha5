# Platform 10 Plugin Lifecycle Specification

All methodology plugins executed by Platform 10 must conform to the following strict lifecycle sequence:

1. **Discovery**: The Plugin Loader scans the `Backend/Platform10/plugins/` directory for registered methodologies.
2. **Registry Validation**: The loader cross-references the discovered plugin with the Project OS `master_capability_registry.yaml`. If the `lifecycle_status` is `frozen` or `disabled`, discovery is aborted.
3. **Instantiation**: The engine injects required dependencies and creates the plugin instance.
4. **Configuration**: Universal Switch overrides are applied (e.g. timeframe or asset class bounds).
5. **Execution**: The `evaluate(MarketStateDTO)` method is invoked. **The Execution Context guarantees immutable inputs, deterministic processing, and no network/DB access.**
6. **Evidence Generation**: The plugin compiles supporting and conflicting concept data.
7. **Scoring**: Internal logic calculates Confidence and Strength.
8. **Validation**: The engine applies bounds checking to ensure values are normalized (0.0 to 1.0).
9. **MethodologyResultDTO**: The final typed data object is instantiated.
10. **Unload**: The plugin instance releases any cache allocations.
