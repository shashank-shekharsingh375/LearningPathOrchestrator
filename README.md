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

The current prototype uses local JSON catalogs in `data/`. Foundry model integration can be added behind the agent and workflow boundaries in `app/`.
