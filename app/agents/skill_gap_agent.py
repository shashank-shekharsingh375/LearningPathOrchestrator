import asyncio
import json
from typing import Any

from app.foundry.settings import FoundrySettings
from app.models.employee import EmployeeProfile
from app.models.skill_gap import SkillGapAnalysis
from app.tools.role_catalog_tool import RoleCatalogTool


class FoundrySkillGapAgent:
    """Agent Framework wrapper for a Foundry-hosted skill-gap agent."""

    def __init__(self, data_dir: str, settings: FoundrySettings | None = None):
        self.role_catalog = RoleCatalogTool(data_dir)
        self.settings = settings or FoundrySettings.from_environment()

    def _prompt(self, employee: EmployeeProfile, role_profile: dict[str, Any]) -> str:
        return json.dumps({
            "task": "Analyze the employee skill gap for the target role.",
            "employee": employee.to_dict(),
            "target_role_profile": role_profile,
            "required_output": {
                "current_skills": ["string"],
                "required_skills": ["string"],
                "missing_skills": ["string"],
                "priority_score": "integer from 1 to 100",
                "summary": "string",
            },
        })

    async def _run_foundry_agent(self, prompt: str) -> dict[str, Any]:
        if not self.settings.agent_name:
            raise ValueError(
                "FOUNDRY_AGENT_NAME is required to invoke the Foundry-backed agent."
            )

        from agent_framework_foundry import FoundryAgent
        from azure.identity import DefaultAzureCredential

        agent = FoundryAgent(
            project_endpoint=self.settings.project_endpoint,
            agent_name=self.settings.agent_name,
            agent_version=self.settings.agent_version,
            credential=DefaultAzureCredential(),
        )
        response = await agent.run(prompt)
        text = getattr(response, "text", "")
        return json.loads(text)

    def analyze_employee(self, employee: EmployeeProfile) -> SkillGapAnalysis:
        role_profile = self.role_catalog.get_role_profile(employee.target_role)
        result = asyncio.run(self._run_foundry_agent(self._prompt(employee, role_profile)))
        return SkillGapAnalysis(
            current_role=employee.current_role,
            target_role=employee.target_role,
            current_skills=result["current_skills"],
            required_skills=result["required_skills"],
            missing_skills=result["missing_skills"],
            priority_score=int(result["priority_score"]),
            summary=result["summary"],
        )