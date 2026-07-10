from typing import Dict
from Backend.core.methodologies.rules.sdk.base_rule import BaseEvidenceRule

class EvidenceRuleRegistry:
    """The central catalog mapping string IDs to singleton rule implementations."""
    
    def __init__(self):
        self._rules: Dict[str, BaseEvidenceRule] = {}
        
    def register(self, rule: BaseEvidenceRule):
        self._rules[rule.rule_id] = rule
        
    def get_rule(self, rule_id: str) -> BaseEvidenceRule:
        if rule_id not in self._rules:
            raise KeyError(f"Rule {rule_id} not found in Registry.")
        return self._rules[rule_id]
