import json
from pathlib import Path
from typing import List

from app.models.skill_gap import SkillGapAnalysis
from app.models.employee import EmployeeProfile


class SkillGapAnalyzer:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.role_catalog = self._load_json("roles.json")

    def _load_json(self, file_name: str) -> dict:
        with open(self.data_dir / file_name, "r", encoding="utf-8") as file:
            return json.load(file)

    def _infer_current_skills(self, employee: EmployeeProfile) -> List[str]:
        skill_map = {
            "Software Engineer": ["Python", "Software development", "APIs", "Debugging"],
            "Data Analyst": ["Data analysis", "SQL", "Visualization", "Python"],
            "Cloud Engineer": ["Azure", "Networking", "Linux", "Infrastructure as code"],
            "Developer": ["Programming", "APIs", "Testing", "Git"],
        }
        return skill_map.get(employee.current_role, ["General technical skills", "Problem solving"])

    def analyze_employee(self, employee: EmployeeProfile) -> SkillGapAnalysis:
        target_profile = self.role_catalog.get(employee.target_role, {})
        required = target_profile.get("required_skills", [])
        current = self._infer_current_skills(employee)
        missing = [skill for skill in required if skill not in current]

        # Simple priority scoring based on gap size and current experience
        priority_score = max(1, len(missing) * 15 + (1 if employee.experience_level.lower() in {"junior", "mid"} else 0))

        summary = (
            f"{employee.current_role} is targeting {employee.target_role}. "
            f"The analysis found {len(missing)} key missing capabilities across the required Azure and AI skill set."
        )

        return SkillGapAnalysis(
            current_role=employee.current_role,
            target_role=employee.target_role,
            current_skills=current,
            required_skills=required,
            missing_skills=missing,
            priority_score=priority_score,
            summary=summary,
        )
