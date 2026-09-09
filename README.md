# Learning Path Orchestrator

A FastAPI prototype that creates Azure and AI learning journeys with skill-gap analysis, curated learning resources, weekly planning, and manager approval.

## Run locally

From the parent workspace:

```powershell
$env:PYTHONPATH = "$PWD\LearningPathOrchestrator"
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000.

## Workflow

1. Submit an employee profile.
2. Review the generated skill gaps and learning resources.
3. Review the weekly plan as a manager.
4. Approve the pathway or request changes.

The `hybrid_approach` branch adds the first Foundry + Agent Framework boundary:

- `app/agents/skill_gap_agent.py` invokes a configured Foundry agent through Agent Framework.
- `app/tools/role_catalog_tool.py` keeps role data deterministic and local.
- `app/workflows/hybrid_learning_workflow.py` combines the Foundry agent with the existing curator and planner.
- `app/persistence/sqlite_repository.py` persists plans while they await manager approval.

## Enable the hybrid slice

1. Create a Prompt Agent in the Microsoft Foundry project and note its name and version.
2. Copy `.env.example` to `.env`.
3. Set `FOUNDRY_PROJECT_ENDPOINT`, `MODEL_DEPLOYMENT_NAME`, `FOUNDRY_AGENT_NAME`, and optionally `FOUNDRY_AGENT_VERSION`.
4. Authenticate locally with Azure CLI:

```powershell
az login
```

5. Invoke `HybridLearningPathWorkflow` from Python or wire it into the FastAPI route after validating the Foundry agent response schema.

The current browser route remains on the deterministic workflow until the Foundry agent is configured. This keeps the local UI runnable while the hybrid slice is tested independently.
