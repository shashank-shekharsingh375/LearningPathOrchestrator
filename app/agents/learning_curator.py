import json
from pathlib import Path
from typing import List, Dict, Any


class LearningCurator:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.xprojects = self._load_json("xprojects.json")

    def _load_json(self, file_name: str):
        with open(self.data_dir / file_name, "r", encoding="utf-8") as file:
            return json.load(file)

    def curate_modules(self, missing_skills: List[str], target_role: str) -> List[Dict[str, Any]]:
        modules = []

        for skill in missing_skills:
            if "Azure AI" in skill or "AI services" in skill or "Generative AI" in skill:
                modules.append({
                    "title": f"Learn {skill} on Microsoft Learn",
                    "source_type": "learn",
                    "url": "https://learn.microsoft.com/training/browse/?products=azure",
                    "duration_weeks": 2,
                    "focus_skill": skill,
                })
            elif "Azure OpenAI" in skill:
                modules.append({
                    "title": "Azure OpenAI Fundamentals",
                    "source_type": "learn",
                    "url": "https://learn.microsoft.com/training/paths/integrate-azure-openai/",
                    "duration_weeks": 2,
                    "focus_skill": skill,
                })
            elif "Azure ML" in skill:
                modules.append({
                    "title": "Azure Machine Learning essentials",
                    "source_type": "learn",
                    "url": "https://learn.microsoft.com/training/paths/build-ai-solutions-with-azure-machine-learning/",
                    "duration_weeks": 2,
                    "focus_skill": skill,
                })

        for project in self.xprojects:
            if project.get("role") == target_role:
                modules.append({
                    "title": project["title"],
                    "source_type": "xproject",
                    "url": project.get("url", ""),
                    "duration_weeks": 3,
                    "focus_skill": project["skills"][0] if project.get("skills") else "project delivery",
                    "description": project.get("description", ""),
                })

        if not modules:
            modules.append({
                "title": f"Foundational learning path for {target_role}",
                "source_type": "learn",
                "url": "https://learn.microsoft.com/training/",
                "duration_weeks": 2,
                "focus_skill": "career readiness",
            })

        return modules
