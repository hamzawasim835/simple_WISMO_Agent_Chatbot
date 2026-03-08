from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import os
from agent import get_order_status, process_returns # Import your logic

app = FastAPI()
script_dir = os.path.dirname(os.path.abspath(__file__))

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def read_index():
    # This ensures it finds the file in the same directory as app.py
    path = os.path.join(os.path.dirname(__file__), "index.html")
    return FileResponse(path)

@app.post("/chat")
async def chat(req: ChatRequest):
    # This is where you call your agent
    # response = agent_executor.invoke({"input": req.message})
    # return {"reply": response["output"]}
    
    # Placeholder for your vibe-coding logic:
    return {"reply": "Agent is processing: " + req.message}