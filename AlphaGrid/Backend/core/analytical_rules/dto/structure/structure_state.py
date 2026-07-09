from dataclasses import dataclass, field
from typing import List, Dict, Optional
from Backend.core.analytical_rules.dto.state_evidence_dto import StateEvidenceDTO

from Backend.core.analytical_rules.dto.structure.structure_graph_dto import StructureGraphDTO
from Backend.core.analytical_rules.dto.structure.swing_identity_dto import SwingIdentityDTO

@dataclass(frozen=True)
class StructureState(StateEvidenceDTO):
    """
    Maintains the geometric map of the market using immutable swing IDs.
    Excludes subjective fields like trend or bias.
    """
    graph_namespaces: Dict[str, StructureGraphDTO] = field(default_factory=dict)
    swing_identities: Dict[str, SwingIdentityDTO] = field(default_factory=dict)
    
    # Store latest highs/lows per policy
    latest_confirmed_high_ids: Dict[str, str] = field(default_factory=dict)
    latest_confirmed_low_ids: Dict[str, str] = field(default_factory=dict)
