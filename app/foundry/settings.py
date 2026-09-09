import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class FoundrySettings:
    project_endpoint: str
    model_deployment_name: str
    agent_name: str | None = None
    agent_version: str | None = None

    @classmethod
    def from_environment(cls) -> "FoundrySettings":
        load_dotenv()
        endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT", "").strip()
        deployment = os.getenv("MODEL_DEPLOYMENT_NAME", "").strip()
        if not endpoint or not deployment:
            raise ValueError(
                "FOUNDRY_PROJECT_ENDPOINT and MODEL_DEPLOYMENT_NAME must be configured."
            )
        return cls(
            project_endpoint=endpoint,
            model_deployment_name=deployment,
            agent_name=os.getenv("FOUNDRY_AGENT_NAME", "").strip() or None,
            agent_version=os.getenv("FOUNDRY_AGENT_VERSION", "").strip() or None,
        )