# mcp_server.py

import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ContextRequest(BaseModel):
    user_id: str
    message: str

@app.get("/")
def root():
    return {"message": "MCP Server is running."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/process")
def process_context(data: ContextRequest):
    return {
        "user_id": data.user_id,
        "original_message": data.message,
        "response": f"Echo: {data.message}",
        "openai_api_key_used":   os.getenv("OPENAI_API_KEY", "N/A")[:6],
        "gemini_api_key_used":   os.getenv("GEMINI_API_KEY", "N/A")[:6],
        "deepseek_api_key_used": os.getenv("DEEPSEEK_API_KEY", "N/A")[:6],

    }