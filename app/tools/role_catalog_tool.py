import json
from pathlib import Path
from typing import Any


class RoleCatalogTool:
    """Trusted local lookup for target-role competency requirements."""

    def __init__(self, data_dir: str):
        with open(Path(data_dir) / "roles.json", "r", encoding="utf-8") as file:
            self.roles: dict[str, dict[str, Any]] = json.load(file)

    def get_role_profile(self, target_role: str) -> dict[str, Any]:
        profile = self.roles.get(target_role)
        if profile is None:
            raise ValueError(f"Target role is not in the catalog: {target_role}")
        return {"role": target_role, **profile}