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
        # Import the executor from your agent file
        from agent import agent_executor 
        
        # Invoke the agent with the user's message
        response = agent_executor.invoke({"input": req.message})
        
        # Return the actual output from the LLM
        return {"reply": response["output"]}
        
    except Exception as e:
        # If something breaks (like an API key issue), show the error
        print(f"Deployment Error: {e}")
        return {"reply": f"Sorry, I ran into an error: {str(e)}"}