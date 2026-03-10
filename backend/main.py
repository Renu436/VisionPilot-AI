
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
try:
    from .agent import VisionPilotAgent
except ImportError:
    from agent import VisionPilotAgent

app = FastAPI()

agent = None

class Task(BaseModel):
    goal: str


def get_agent():
    global agent
    if agent is None:
        agent = VisionPilotAgent()
    return agent


@app.post("/run-agent")
def run_agent(task: Task):

    try:
        result = get_agent().run(task.goal)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {"result": result}
