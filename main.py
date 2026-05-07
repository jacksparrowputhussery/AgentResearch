from fastapi import FastAPI
from pydantic import BaseModel

from pipeline import run_research_pipeline

app = FastAPI()


class ResearchRequest(BaseModel):
    topic: str


@app.get("/")
def home():
    return {"message": "Multi-Agent Research API Running"}


@app.post("/research")
def research(request: ResearchRequest):

    result = run_research_pipeline(request.topic)

    return {
        "topic": request.topic,
        "report": result["report"],
        "feedback": result["feedback"]
    }