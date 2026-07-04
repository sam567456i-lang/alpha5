from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class RepositoryState:
    python_files: List[str] = field(default_factory=list)
    markdown_files: List[str] = field(default_factory=list)
    yaml_files: List[str] = field(default_factory=list)
    csv_files: List[str] = field(default_factory=list)
    
@dataclass
class ProjectMemory:
    bible_content: str = ""
    roadmap_content: str = ""
    capability_registry: Dict[str, Any] = field(default_factory=dict)
    capability_matrix: List[Dict[str, str]] = field(default_factory=list)
    validation_registry: Dict[str, Any] = field(default_factory=dict)
    adrs: Dict[str, str] = field(default_factory=dict)

@dataclass
class AnalysisReport:
    gap_analysis: Dict[str, Any] = field(default_factory=dict)
    risk_analysis: Dict[str, Any] = field(default_factory=dict)
    impact_analysis: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[Dict[str, Any]] = field(default_factory=list)
    readiness_scores: Dict[str, float] = field(default_factory=dict)

@dataclass
class ImplementationPlan:
    next_task: str
    platform: str
    dependencies_satisfied: bool
    required_validators: List[str]
    estimated_effort: str
    risk_level: str
    execution_sequence: List[str]
