from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class EmployeeProfile:
    current_role: str
    experience_level: str
    certifications: List[str] = field(default_factory=list)
    target_role: str = ""
    manager_name: Optional[str] = None
    notes: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "current_role": self.current_role,
            "experience_level": self.experience_level,
            "certifications": self.certifications,
            "target_role": self.target_role,
            "manager_name": self.manager_name,
            "notes": self.notes,
        }
