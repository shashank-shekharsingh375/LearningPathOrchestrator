import json
import sqlite3
from pathlib import Path
from typing import Any


class SqliteWorkflowRepository:
    """Small local repository for workflow state and manager decisions."""

    def __init__(self, database_path: str):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS workflow_state (
                    workflow_id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    payload TEXT NOT NULL
                )"""
            )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_path)

    def save(self, workflow_id: str, status: str, payload: dict[str, Any]) -> None:
        with self._connect() as connection:
            connection.execute(
                "INSERT OR REPLACE INTO workflow_state VALUES (?, ?, ?)",
                (workflow_id, status, json.dumps(payload)),
            )

    def get(self, workflow_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT status, payload FROM workflow_state WHERE workflow_id = ?",
                (workflow_id,),
            ).fetchone()
        if row is None:
            return None
        return {"status": row[0], "payload": json.loads(row[1])}

    def update_status(self, workflow_id: str, status: str, approval: dict[str, Any]) -> None:
        stored = self.get(workflow_id)
        if stored is None:
            raise KeyError(f"Unknown workflow: {workflow_id}")
        if stored["status"] != "AWAITING_MANAGER_APPROVAL":
            raise ValueError(f"Workflow is not awaiting approval: {workflow_id}")
        payload = stored["payload"]
        payload["approval"] = approval
        payload["status"] = status
        self.save(workflow_id, status, payload)