from abc import ABC, abstractmethod
from typing import List, Any
from Backend.core.methodology.policy_identity import PolicyIdentity

class MethodologyProfile(ABC):
    """
    Base class for any methodology (ICT, SMC, Wyckoff, MMXM).
    A profile is a collection of versioned policies and execution capabilities
    that translate objective Platform 10 evidence into subjective Platform 11 narratives.
    """
    
    @property
    @abstractmethod
    def profile_name(self) -> str:
        pass
        
    @property
    @abstractmethod
    def version(self) -> str:
        pass
        
    @abstractmethod
    def get_policies(self) -> List[Any]:
        """Returns the specific interpretation policies used by this methodology."""
        pass
        
    @abstractmethod
    def get_identity(self) -> PolicyIdentity:
        pass
