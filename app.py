from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()   # loads .env locally; on Render env vars are set in the dashboard
from run_llm import run_llm
import json
import uvicorn

app = FastAPI(title="Sales Agent API")

# ─── Helper ────────────────────────────────────────────────────
def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ─── Pydantic Models ───────────────────────────────────────────
class QueryModel(BaseModel):
    query: str

# ─── CRM Data Endpoints ────────────────────────────────────────
@app.get("/api/crm/deals")
def get_all_deals():
    return load_json("CRM/deals.json")

@app.get("/api/crm/accounts")
def get_all_accounts():
    return load_json("CRM/accounts.json")

@app.get("/api/crm/contacts")
def get_all_contacts():
    return load_json("CRM/contacts.json")

@app.get("/api/crm/tasks")
def get_all_tasks():
    return load_json("CRM/tasks.json")

@app.get("/api/crm/meetings")
def get_all_meetings():
    return load_json("CRM/meetings.json")

@app.get("/api/crm/emails")
def get_all_emails():
    return load_json("CRM/emails.json")

@app.get("/api/crm/users")
def get_all_users():
    return load_json("CRM/users.json")

# ─── AI Agent Endpoint ─────────────────────────────────────────
@app.post("/api/query")
def process_query(req: QueryModel):
    try:
        result = run_llm(req.query)
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ─── Frontend ──────────────────────────────────────────────────
@app.get("/")
def read_index():
    return FileResponse("index.html")

# ─── Run ───────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
