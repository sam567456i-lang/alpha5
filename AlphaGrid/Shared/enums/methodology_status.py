"""Methodology status enumerations."""

from enum import StrEnum

class MethodologyStatus(StrEnum):
    EXPERIMENTAL = "EXPERIMENTAL"
    VALIDATED = "VALIDATED"
    DEPRECATED = "DEPRECATED"
