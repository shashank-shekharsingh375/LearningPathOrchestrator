from pathlib import Path

from app.agents.gap_analyzer import SkillGapAnalyzer
from app.agents.learning_curator import LearningCurator
from app.agents.study_planner import StudyPlanner
from app.approval.manager_approval import ApprovalManager
from app.models.employee import EmployeeProfile


class LearningPathWorkflow:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.gap_analyzer = SkillGapAnalyzer(data_dir=data_dir)
        self.curator = LearningCurator(data_dir=data_dir)
        self.planner = StudyPlanner()
        self.approval_manager = ApprovalManager()

    def run(
        self,
        employee: EmployeeProfile,
        manager_name: str = "Manager",
        manager_decision: str = "Under Review",
        manager_notes: str = "",
    ):
        gap = self.gap_analyzer.analyze_employee(employee)
        modules = self.curator.curate_modules(gap.missing_skills, employee.target_role)
        learning_plan = self.planner.build_plan(modules, employee.target_role)

        decision = self.approval_manager.decide(
            manager_decision,
            manager_notes or f"Plan submitted to {manager_name} for review.",
        )

        return {
            "status": decision["status"],
            "employee": employee.to_dict(),
            "gap_analysis": gap.to_dict(),
            "learning_plan": learning_plan.to_dict(),
            "risk_summary": {
                "missing_skills": gap.missing_skills,
                "estimated_weeks": learning_plan.total_weeks,
                "approval_status": decision["status"],
            },
        }
