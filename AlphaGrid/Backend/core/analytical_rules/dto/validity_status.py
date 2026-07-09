from enum import Enum

class ValidityStatus(Enum):
    GENERATED = "generated"
    VALIDATED = "validated"
    ACTIVE = "active"
    SUPERSEDED = "superseded"
    INVALIDATED = "invalidated"
    EXPIRED = "expired"
    ARCHIVED = "archived"
