"""Data Validator — ensures raw records are sane before normalisation."""

from __future__ import annotations

from .providers.base import OHLCVRecord, ValidationResult, ValidationStatus


class OHLCVValidator:
    """Validates raw OHLCV records from providers."""

    @staticmethod
    def validate(record: OHLCVRecord) -> ValidationResult:
        """Validate a single OHLCV record.

        Rules:
        1. High must be >= Open and >= Close
        2. Low must be <= Open and <= Close
        3. High must be >= Low
        4. Volume must be >= 0
        """
        if record.high < record.open or record.high < record.close:
            return ValidationResult(
                ValidationStatus.FAIL,
                f"High ({record.high}) is lower than Open ({record.open}) or Close ({record.close})",
            )

        if record.low > record.open or record.low > record.close:
            return ValidationResult(
                ValidationStatus.FAIL,
                f"Low ({record.low}) is higher than Open ({record.open}) or Close ({record.close})",
            )

        if record.high < record.low:
            return ValidationResult(
                ValidationStatus.FAIL,
                f"High ({record.high}) is lower than Low ({record.low})",
            )

        if record.volume < 0:
            return ValidationResult(
                ValidationStatus.FAIL,
                f"Volume ({record.volume}) is negative",
            )

        return ValidationResult(ValidationStatus.PASS)

    @classmethod
    def validate_all(cls, records: list[OHLCVRecord]) -> list[OHLCVRecord]:
        """Validate a batch of records, returning only those that pass."""
        passed: list[OHLCVRecord] = []
        for r in records:
            result = cls.validate(r)
            if result.status == ValidationStatus.PASS:
                passed.append(r)
            # In a full production system, failed records would be sent to Quarantine
        return passed
