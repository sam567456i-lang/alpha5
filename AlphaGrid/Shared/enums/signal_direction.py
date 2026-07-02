"""Signal direction enumerations."""

from enum import StrEnum

class SignalDirection(StrEnum):
    LONG = "LONG"
    SHORT = "SHORT"
    WAIT = "WAIT"
