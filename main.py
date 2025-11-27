import os
import urllib.parse
from fastapi import FastAPI, Request, Form
from fastapi.responses import Response, StreamingResponse
from twilio.twiml.voice_response import VoiceResponse
from dotenv import load_dotenv
from services.voice_service import generate_speech

# Load environment variables
load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hotel Agent is running"}

@app.get("/speak")
async def speak(text: str):
    """
    Returns audio stream for the given text using ElevenLabs.
    """
    audio_stream = generate_speech(text)
    if not audio_stream:
        return Response(content="Error generating audio", status_code=500)
    
    # ElevenLabs returns a generator, StreamingResponse handles it
    return StreamingResponse(audio_stream, media_type="audio/mpeg")

@app.post("/incoming-call")
async def incoming_call(request: Request):
    """
    Handle incoming calls from Twilio.
    """
    response = VoiceResponse()
    
    welcome_text = "Welcome to the Hotel Agent. This is an Eleven Labs voice. How can I help you?"
    
    # Use ElevenLabs audio
    # Note: In production, ensure the URL is absolute or correctly resolved by Twilio
    encoded_text = urllib.parse.quote(welcome_text)
    response.play(f"/speak?text={encoded_text}")
    
    # Fallback to Gather for user input (placeholder)
    # gather = response.gather(input="speech", action="/handle-speech")
    
    return Response(content=str(response), media_type="application/xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
