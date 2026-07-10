from dataclasses import dataclass, field
from typing import List

@dataclass
class RequiredPDArray:
    array_type: str # e.g. "FVG", "OB", "Breaker"
    classification: str = "" # e.g. "Discount", "Premium", "" (any)

@dataclass
class ConfluenceConfiguration:
    name: str
    required_pd_arrays: List[RequiredPDArray] = field(default_factory=list)

@dataclass
class ICTConfluencePolicy:
    """
    Evaluates ConfluenceCandidateNodes against a set of supported configurations.
    """
    configurations: List[ConfluenceConfiguration] = field(default_factory=lambda: [
        ConfluenceConfiguration(
            name="UNICORN",
            required_pd_arrays=[
                RequiredPDArray(array_type="FVG"),
                RequiredPDArray(array_type="Breaker")
            ]
        ),
        ConfluenceConfiguration(
            name="DOUBLE_FVG",
            required_pd_arrays=[
                RequiredPDArray(array_type="FVG"),
                RequiredPDArray(array_type="FVG")
            ]
        )
    ])
