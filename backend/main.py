
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
try:
    from .agent import VisionPilotAgent
except ImportError:
    from agent import VisionPilotAgent

app = FastAPI()

class Task(BaseModel):
    goal: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/run-agent")
def run_agent(task: Task):
    agent = VisionPilotAgent()

    try:
        result = agent.run(task.goal)
    except RuntimeError as exc:
        return {"status": "error", "message": str(exc), "results": []}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        agent.close()

    return result
