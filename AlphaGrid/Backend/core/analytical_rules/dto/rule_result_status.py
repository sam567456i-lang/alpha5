from enum import Enum, auto

class RuleResultStatus(Enum):
    SUCCESS = "SUCCESS"
    PARTIAL = "PARTIAL"
    SKIPPED = "SKIPPED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"
    INSUFFICIENT_INPUT = "INSUFFICIENT_INPUT"
