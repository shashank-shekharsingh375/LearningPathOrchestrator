import json
from pathlib import Path

from app.agents.gap_analyzer import SkillGapAnalyzer
from app.agents.learning_curator import LearningCurator
from app.agents.study_planner import StudyPlanner
from app.approval.manager_approval import ApprovalManager, ApprovalStatus
from app.models.employee import EmployeeProfile
from app.workflows.learning_workflow import LearningPathWorkflow


ROOT = Path(__file__).resolve().parents[1]


def test_gap_analysis_for_azure_ai_engineer():
    employee = EmployeeProfile(
        current_role="Software Engineer",
        experience_level="Mid",
        certifications=["AZ-900"],
        target_role="Azure AI Engineer",
    )

    analyzer = SkillGapAnalyzer(data_dir=str(ROOT / "data"))
    result = analyzer.analyze_employee(employee)

    assert result.missing_skills
    assert "Azure AI services" in result.missing_skills or "Azure AI" in " ".join(result.missing_skills)
    assert result.priority_score > 0


def test_curator_returns_learning_modules():
    curator = LearningCurator(data_dir=str(ROOT / "data"))
    modules = curator.curate_modules(["Azure AI services", "Generative AI", "Python for Azure"], target_role="Azure AI Engineer")

    assert modules
    assert all("title" in module for module in modules)
    assert any(module["source_type"] in {"learn", "xproject"} for module in modules)


def test_planner_creates_weekly_plan():
    planner = StudyPlanner()
    modules = [
        {"title": "Azure AI Fundamentals", "duration_weeks": 2},
        {"title": "Azure OpenAI", "duration_weeks": 2},
        {"title": "Responsible AI", "duration_weeks": 1},
    ]

    plan = planner.build_plan(modules, target_role="Azure AI Engineer")

    assert plan.weekly_plan
    assert len(plan.weekly_plan) >= 3
    assert plan.total_weeks >= 3


def test_manager_approval_workflow():
    approval = ApprovalManager()
    decision = approval.decide("Approved", "Looks good for the role transition")

    assert decision["status"] == ApprovalStatus.APPROVED
    assert "Looks good" in decision["notes"]


def test_full_learning_path_workflow():
    employee = EmployeeProfile(
        current_role="Data Analyst",
        experience_level="Junior",
        certifications=["PL-300"],
        target_role="Azure AI Engineer",
    )

    workflow = LearningPathWorkflow(data_dir=str(ROOT / "data"))
    result = workflow.run(employee, manager_name="Priya")

    assert result["status"] in {"Approved", "Under Review", "Rejected"}
    assert "learning_plan" in result
    assert "risk_summary" in result
