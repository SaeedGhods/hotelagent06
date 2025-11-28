import os
import urllib.parse
import logging
from fastapi import FastAPI, Request, Form
from fastapi.responses import Response, StreamingResponse
from twilio.twiml.voice_response import VoiceResponse, Gather
from dotenv import load_dotenv
from services.voice_service import generate_speech
from services.llm_service import get_ai_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
    logger.info("Health check endpoint called")
    return {"message": "Hotel Agent is running"}

@app.get("/speak")
async def speak(text: str):
    """
    Returns audio stream for the given text using ElevenLabs.
    """
    logger.info(f"Generating speech for: {text}")
    try:
        audio_stream = generate_speech(text)
        if not audio_stream:
            logger.error("Failed to generate speech: No stream returned")
            return Response(content="Error generating audio", status_code=500)
        
        return StreamingResponse(audio_stream, media_type="audio/mpeg")
    except Exception as e:
        logger.error(f"Error in /speak: {str(e)}")
        return Response(content=f"Internal Server Error: {str(e)}", status_code=500)

@app.post("/incoming-call")
async def incoming_call(request: Request):
    """
    Handle incoming calls from Twilio.
    Starts the conversation.
    """
    logger.info("Incoming call received")
    
    # ---------------------------------------------------------
    # EMERGENCY DEBUG MODE
    # If this still fails, the issue is fundamental (e.g. imports)
    # ---------------------------------------------------------
    try:
        response = VoiceResponse()
        # ABSOLUTE SIMPLEST RESPONSE POSSIBLE
        # No variables, no ElevenLabs, no logic. Just XML.
        response.say("Hello. If you can hear this, the connection is working.")
        
        xml_str = str(response)
        logger.info(f"Returning XML: {xml_str}")
        return Response(content=xml_str, media_type="application/xml")
    except Exception as e:
        logger.error(f"CRITICAL ERROR in /incoming-call: {str(e)}")
        return Response(content="<?xml version='1.0' encoding='UTF-8'?><Response><Say>System Failure</Say></Response>", media_type="application/xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
