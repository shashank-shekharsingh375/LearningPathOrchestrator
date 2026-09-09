from uuid import uuid4

from app.agents.learning_curator import LearningCurator
from app.agents.skill_gap_agent import FoundrySkillGapAgent
from app.agents.study_planner import StudyPlanner
from app.models.employee import EmployeeProfile
from app.persistence.sqlite_repository import SqliteWorkflowRepository


class HybridLearningPathWorkflow:
    """Agent Framework/Foundry boundary with deterministic local tools around it."""

    def __init__(self, data_dir: str, database_path: str, gap_agent=None):
        self.gap_agent = gap_agent or FoundrySkillGapAgent(data_dir=data_dir)
        self.curator = LearningCurator(data_dir=data_dir)
        self.planner = StudyPlanner()
        self.repository = SqliteWorkflowRepository(database_path)

    def create_draft(self, employee: EmployeeProfile) -> dict:
        workflow_id = str(uuid4())
        gap = self.gap_agent.analyze_employee(employee)
        modules = self.curator.curate_modules(gap.missing_skills, employee.target_role)
        plan = self.planner.build_plan(modules, employee.target_role)
        payload = {
            "workflow_id": workflow_id,
            "employee": employee.to_dict(),
            "gap_analysis": gap.to_dict(),
            "learning_plan": plan.to_dict(),
            "risk_summary": {
                "missing_skills": gap.missing_skills,
                "estimated_weeks": plan.total_weeks,
            },
        }
        self.repository.save(workflow_id, "AWAITING_MANAGER_APPROVAL", payload)
        return {"status": "AWAITING_MANAGER_APPROVAL", **payload}