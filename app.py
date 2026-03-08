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
    try:
        # 1. Call your Agent (Ensure 'agent_executor' is defined in agent.py and imported)
        from agent import agent_executor 
        
        # 2. Run the invocation
        response = agent_executor.invoke({"input": req.message})
        
        # 3. Return the AI's actual words
        return {"reply": response["output"]}
        
    except Exception as e:
        # This helps you debug in the UI if the API key or Agent fails
        print(f"Error in chat endpoint: {e}")
        return {"reply": f"Agent Error: {str(e)}"}