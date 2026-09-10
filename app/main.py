from pathlib import Path

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

from app.models.employee import EmployeeProfile
from app.workflows.hybrid_learning_workflow import HybridLearningPathWorkflow


APP_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = APP_ROOT / "data"
workflow = HybridLearningPathWorkflow(
  data_dir=str(DATA_DIR),
  database_path=str(DATA_DIR / "workflow.db"),
)
app = FastAPI(title="Learning Path Orchestrator")


def esc(value: object) -> str:
    text = str(value)
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;").replace("'", "&#x27;"))


def render_page(result: dict | None = None, error: str = "") -> str:
    result_markup = ""
    if result:
        gap = result["gap_analysis"]
        plan = result["learning_plan"]
        status = result["status"]
        status_class = status.lower().replace(" ", "-")
        weeks = "".join(
            f"<article class='week'><span>WEEK {item['week']:02d}</span>"
            f"<h3>{esc(item['module'])}</h3><p>{esc(item['focus'])}</p>"
            f"<small>{item['estimated_hours']} hours · {esc(item['deliverable'])}</small></article>"
            for item in plan["weekly_plan"]
        )
        modules = "".join(
            f"<li><a href='{esc(module['url'])}' target='_blank' rel='noreferrer'>"
            f"{esc(module['title'])}</a><span>{esc(module['source_type'])}</span></li>"
            for module in plan["recommended_modules"]
        )
        result_markup = f"""
        <section class='results'>
          <div class='result-head'><div><p class='eyebrow'>PATHWAY GENERATED</p>
            <h2>{esc(plan['target_role'])}</h2><p>{esc(gap['summary'])}</p></div>
            <strong class='status {status_class}'>{esc(status)}</strong></div>
          <div class='metrics'><div><b>{len(gap['missing_skills'])}</b><span>priority gaps</span></div>
            <div><b>{plan['total_weeks']}</b><span>estimated weeks</span></div>
            <div><b>{len(plan['recommended_modules'])}</b><span>resources</span></div></div>
          <div class='columns'><div><h3>Skill gaps</h3><div class='chips'>
            {''.join(f"<span>{esc(skill)}</span>" for skill in gap['missing_skills'])}</div></div>
            <div><h3>Learning resources</h3><ul class='resources'>{modules}</ul></div></div>
          <h3 class='section-title'>Weekly study plan</h3><div class='weeks'>{weeks}</div>
          <form class='approval' method='post' action='/review'><input type='hidden' name='workflow_id' value='{esc(result['workflow_id'])}'>
            <label>Manager notes <textarea name='notes' placeholder='Add guidance for the learner'></textarea></label>
            <div class='actions'><button name='decision' value='Rejected' class='secondary'>Request changes</button>
              <button name='decision' value='Approved'>Approve pathway</button></div></form>
        </section>"""
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'>
      <meta name='viewport' content='width=device-width, initial-scale=1'><title>Learning Path Orchestrator</title>
      <style>{STYLES}</style></head><body><main><header><div class='brand'>LP<span>O</span></div>
        <div><p class='eyebrow'>CAREER ENABLEMENT / HUMAN REVIEW</p><h1>Build a learning path<br><em>with a clear next step.</em></h1></div></header>
        <section class='intro'><p>Turn an employee's current experience into a focused Azure and AI journey, then send it through a manager approval gate.</p></section>
        {f"<div class='error'>{esc(error)}</div>" if error else ""}
        <section class='form-panel'><div><p class='eyebrow'>EMPLOYEE PROFILE</p><h2>Start with the essentials</h2></div>
        <form method='post' action='/generate'><div class='form-grid'>
          <label>Current role<input name='current_role' required placeholder='e.g. Data Analyst'></label>
          <label>Experience level<select name='experience_level'><option>Junior</option><option selected>Mid</option><option>Senior</option></select></label>
          <label>Certifications<input name='certifications' placeholder='e.g. PL-300, AZ-900'></label>
          <label>Target role<input name='target_role' required placeholder='e.g. Azure AI Engineer'></label>
          <label>Manager name<input name='manager_name' value='Manager'></label></div>
          <button type='submit'>Generate pathway <span>→</span></button></form></section>{result_markup}
      </main></body></html>"""


@app.get("/", response_class=HTMLResponse)
def home():
    return render_page()


@app.post("/generate", response_class=HTMLResponse)
def generate(current_role: str = Form(...), experience_level: str = Form(...), certifications: str = Form(""), target_role: str = Form(...), manager_name: str = Form("Manager")):
    employee = EmployeeProfile(
        current_role=current_role.strip(),
        experience_level=experience_level,
        certifications=[item.strip() for item in certifications.split(",") if item.strip()],
        target_role=target_role.strip(),
        manager_name=manager_name.strip() or "Manager",
    )
    return render_page(workflow.create_draft(employee))


@app.post("/review", response_class=HTMLResponse)
def review(workflow_id: str = Form(...), decision: str = Form(...), notes: str = Form("")):
  result = workflow.review(workflow_id, decision, notes)
  result["risk_summary"]["approval_status"] = result["status"]
  return render_page(result)


STYLES = """
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root{--ink:#172329;--muted:#607078;--paper:#f5f1e9;--line:#d8d4ca;--coral:#e55d45;--mint:#cfe2d3;--blue:#d9e8ed}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:'Space Grotesk',sans-serif}main{max-width:1120px;margin:auto;padding:42px 32px 80px}header{display:flex;gap:56px;align-items:flex-start;border-bottom:1px solid var(--line);padding-bottom:38px}.brand{font-family:'DM Mono',monospace;font-weight:500;font-size:25px;letter-spacing:2px}.brand span{color:var(--coral)}.eyebrow{font-family:'DM Mono',monospace;font-size:11px;letter-spacing:1.5px;color:var(--coral);margin:0 0 14px}h1{font-size:clamp(42px,6vw,78px);line-height:.98;letter-spacing:-2px;margin:0;font-weight:600}h1 em{font-style:normal;color:var(--coral)}h2{font-size:28px;margin:0 0 8px}h3{margin:0 0 12px}.intro{max-width:620px;color:var(--muted);font-size:18px;line-height:1.5;padding:28px 0}.form-panel,.results{border:1px solid var(--ink);padding:30px;background:#fbfaf6}.form-panel{background:var(--mint);display:grid;grid-template-columns:30% 1fr;gap:28px}.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}label{display:flex;flex-direction:column;gap:7px;font-size:13px;font-weight:600}input,select,textarea{font:inherit;border:1px solid var(--ink);background:#fffdf8;padding:13px;color:var(--ink);border-radius:0}textarea{min-height:80px;resize:vertical}.form-panel button,.approval button{margin-top:20px;background:var(--coral);border:1px solid var(--ink);padding:14px 18px;font:600 14px 'Space Grotesk';cursor:pointer;color:var(--ink}.form-panel button span{font-size:20px;margin-left:18px}.results{margin-top:28px}.result-head{display:flex;justify-content:space-between;gap:20px;border-bottom:1px solid var(--line);padding-bottom:24px}.result-head p:not(.eyebrow){color:var(--muted);margin:0}.status{height:max-content;padding:9px 12px;font:500 11px 'DM Mono';white-space:nowrap;border:1px solid var(--ink)}.status.under-review{background:var(--blue)}.status.approved{background:var(--mint)}.status.rejected{background:#f3c2b8}.metrics{display:flex;gap:0;border-bottom:1px solid var(--line);margin-bottom:26px}.metrics div{padding:22px 42px 22px 0;margin-right:42px;border-right:1px solid var(--line)}.metrics b{display:block;font-size:29px}.metrics span{font:11px 'DM Mono';color:var(--muted)}.columns{display:grid;grid-template-columns:1fr 1fr;gap:42px}.chips{display:flex;gap:8px;flex-wrap:wrap}.chips span{background:#f0ddd4;padding:8px 10px;font-size:13px}.resources{list-style:none;margin:0;padding:0}.resources li{border-bottom:1px solid var(--line);padding:9px 0;display:flex;justify-content:space-between;gap:12px}.resources a{color:var(--ink)}.resources span{font:10px 'DM Mono';color:var(--coral)}.section-title{border-top:1px solid var(--line);margin-top:32px;padding-top:24px}.weeks{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px}.week{background:var(--blue);padding:16px;min-height:150px}.week span{font:10px 'DM Mono';color:var(--coral)}.week h3{font-size:16px;margin-top:26px}.week p,.week small{font-size:12px;color:var(--muted);line-height:1.4}.approval{border-top:1px solid var(--line);margin-top:28px;padding-top:22px}.approval textarea{max-width:100%}.actions{display:flex;gap:10px}.approval button{margin-top:12px}.approval .secondary{background:transparent}.error{border:1px solid var(--coral);padding:14px;margin:18px 0;color:var(--coral)}@media(max-width:760px){main{padding:24px 18px 60px}header{gap:22px;flex-direction:column}.form-panel,.columns{display:block}.form-panel>div{margin-bottom:24px}.form-grid{grid-template-columns:1fr}.metrics{overflow:auto}.metrics div{min-width:120px;margin-right:20px;padding-right:20px}.result-head{display:block}.status{display:inline-block;margin-top:18px}.actions{flex-direction:column}.actions button{width:100%}}
"""
