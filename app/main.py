from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from google.genai import errors
from .agent import run_agent

app = FastAPI(title="Support Copilot")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    reply: str
    tools_used: list[str]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        reply, tools_used = run_agent(req.message)
        return ChatResponse(reply=reply, tools_used=tools_used)
    except errors.ClientError as e:
        raise HTTPException(status_code=429, detail="AI quota exceeded, try again later")
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")