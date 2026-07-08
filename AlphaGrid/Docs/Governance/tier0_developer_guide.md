# Tier 0 Analytical Framework Developer Guide

This guide describes how to build, test, and integrate Tier 0 Analytical Rules in AlphaGrid.
Tier 0 rules are the foundational primitives upon which all higher-order Institutional (Tier 1) logic depends. They must be perfectly deterministic, strictly schema-compliant, and fully replayable.

## 1. Core Concepts
* **Determinism**: The same inputs must always produce the same fingerprint and outputs.
* **Sandbox**: Rules cannot access the filesystem, network, databases, or mutable global state.
* **Evidence Classification**: Tier 0 rules ONLY emit `PRIMITIVE` evidence.

## 2. Rule Lifecycle
1. **Instantiation**: Rule is loaded and initialized.
2. **Execution Planning**: The `RuleExecutionPlanner` reads dependencies and schedules execution batches.
3. **Evaluation**: The `evaluate(context)` method is invoked.
4. **Validation**: The emitted `RuleEvidenceDTO` is strictly validated against the Evidence Schema Registry.
5. **Propagation**: Evidence is persisted and propagated to dependent nodes.

## 3. Authoring Guide
Implement rules by inheriting from `AnalyticalRuleSDK`:

```python
from Backend.core.analytical_rules.sdk.analytical_rule_sdk import AnalyticalRuleSDK
from Backend.core.analytical_rules.dto.rule_evidence_dto import RuleEvidenceDTO

class CustomRule(AnalyticalRuleSDK):
    def get_capabilities(self): ...
    def get_dependencies(self): ...
    def fingerprint(self): ...
    def evaluate(self, context) -> RuleEvidenceDTO: ...
    def explain(self, evidence) -> str: ...
```

## 4. Certification Checklist
Before submitting a rule, verify it passes:
- [ ] `test_tier0_functional.py`
- [ ] `test_tier0_contract.py`
- [ ] `test_tier0_replay.py`
- [ ] `test_tier0_sandbox.py` (AST & Runtime)
- [ ] Dependency Audit

## 5. Anti-Patterns
- **Avoid:** Creating custom zones within a rule. (Zones belong in Platform 8).
- **Avoid:** Direct DB connections. (Use context references).
- **Avoid:** Mutating `RuleContextDTO`.

## 6. Migration Guide
When changing a rule's outputs, you must increment the `compatibility_version` and register the change in `rule_evidence_registry.yaml` to pass `test_tier0_migration.py`.
