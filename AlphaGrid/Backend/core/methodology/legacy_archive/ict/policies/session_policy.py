from dataclasses import dataclass, field
from typing import List

@dataclass
class SilverBulletPolicy:
    """Rules for identifying if an ICT Silver Bullet window is active."""
    required_time_windows: List[str] = field(default_factory=lambda: ["10:00-11:00", "14:00-15:00"])
    
@dataclass
class KillzonePolicy:
    """Rules for identifying if an ICT Killzone is active."""
    london_windows: List[str] = field(default_factory=lambda: ["02:00-05:00"])
    new_york_am_windows: List[str] = field(default_factory=lambda: ["08:30-12:00"])
    new_york_pm_windows: List[str] = field(default_factory=lambda: ["13:30-16:00"])
    asian_windows: List[str] = field(default_factory=lambda: ["20:00-00:00"])

@dataclass
class ICTSessionPolicy:
    """
    Configurable ruleset for mapping objective time windows into ICT session concepts.
    """
    silver_bullet: SilverBulletPolicy = field(default_factory=SilverBulletPolicy)
    killzone: KillzonePolicy = field(default_factory=KillzonePolicy)
    
    def is_silver_bullet_active(self, active_windows: List[str]) -> bool:
        return any(w in self.silver_bullet.required_time_windows for w in active_windows)
        
    def get_active_killzones(self, active_windows: List[str]) -> List[str]:
        killzones = []
        if any(w in self.killzone.london_windows for w in active_windows):
            killzones.append("LONDON_KILLZONE")
        if any(w in self.killzone.new_york_am_windows for w in active_windows):
            killzones.append("NEW_YORK_AM_KILLZONE")
        if any(w in self.killzone.new_york_pm_windows for w in active_windows):
            killzones.append("NEW_YORK_PM_KILLZONE")
        if any(w in self.killzone.asian_windows for w in active_windows):
            killzones.append("ASIAN_KILLZONE")
        return killzones
