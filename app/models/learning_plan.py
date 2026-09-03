from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class LearningPlan:
    target_role: str
    total_weeks: int
    weekly_plan: List[Dict[str, Any]] = field(default_factory=list)
    recommended_modules: List[Dict[str, Any]] = field(default_factory=list)
    approval_required: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_role": self.target_role,
            "total_weeks": self.total_weeks,
            "weekly_plan": self.weekly_plan,
            "recommended_modules": self.recommended_modules,
            "approval_required": self.approval_required,
        }
