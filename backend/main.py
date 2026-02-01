from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import whisper
from backend.agents.orchestrator import agent_executor
app = FastAPI(title="Bharat Biz Backend")

# Load Whisper model (Base is fast and good for Hinglish)
# This meets the <5s latency requirement for short clips
model = whisper.load_model("base")

class ChatResponse(BaseModel):
    input_text: str
    agent_output: str

@app.post("/voice-command", response_model=ChatResponse)
async def handle_voice(file: UploadFile = File(...)):
    """
    Receives a Hinglish voice note, transcribes it, 
    and sends the text to the Agentic Orchestrator.
    """
    # 1. Save temporary audio file
    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        buffer.write(await file.read())

    try:
        # 2. Transcribe using Whisper
        # Handles code-mixed inputs like "Rahul ka udhaar chada do"
        result = model.transcribe(temp_filename)
        user_text = result["text"]

        # 3. Process with Agent
        # The orchestrator will decide if it needs to call Udhaar or Inventory tools
        response = agent_executor.invoke({"input": user_text})
        
        return ChatResponse(
            input_text=user_text,
            agent_output=response["output"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Cleanup temp file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

@app.get("/")
def health_check():
    return {"status": "Bharat Biz Backend is running"}