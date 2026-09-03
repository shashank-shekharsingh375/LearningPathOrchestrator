from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class SkillGapAnalysis:
    current_role: str
    target_role: str
    current_skills: List[str] = field(default_factory=list)
    required_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    priority_score: int = 0
    summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "current_role": self.current_role,
            "target_role": self.target_role,
            "current_skills": self.current_skills,
            "required_skills": self.required_skills,
            "missing_skills": self.missing_skills,
            "priority_score": self.priority_score,
            "summary": self.summary,
        }
