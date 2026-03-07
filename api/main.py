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
    # Serves the actual HTML file from the disk
    return FileResponse(os.path.join(script_dir, "index.html"))

@app.post("/chat")
async def chat(req: ChatRequest):
    # This is where you call your agent
    # response = agent_executor.invoke({"input": req.message})
    # return {"reply": response["output"]}
    
    # Placeholder for your vibe-coding logic:
    return {"reply": "Agent is processing: " + req.message}