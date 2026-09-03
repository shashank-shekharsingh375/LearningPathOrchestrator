from typing import List, Dict, Any

from app.models.learning_plan import LearningPlan


class StudyPlanner:
    def build_plan(self, modules: List[Dict[str, Any]], target_role: str) -> LearningPlan:
        total_weeks = sum(item.get("duration_weeks", 1) for item in modules)

        weekly_plan = []
        for index, module in enumerate(modules, start=1):
            weekly_plan.append({
                "week": index,
                "module": module["title"],
                "focus": module.get("focus_skill", "core learning"),
                "deliverable": f"Complete learning and reflection on {module['title']}",
                "estimated_hours": 4,
            })

        return LearningPlan(
            target_role=target_role,
            total_weeks=max(4, total_weeks),
            weekly_plan=weekly_plan,
            recommended_modules=modules,
            approval_required=True,
        )
