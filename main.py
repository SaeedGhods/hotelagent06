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
    return {"message": "Hotel Agent is running"}

@app.get("/speak")
async def speak(text: str):
    """
    Returns audio stream for the given text using ElevenLabs.
    """
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
    try:
        response = VoiceResponse()
        
        hotel_name = os.getenv("HOTEL_NAME", "Grand Hotel")
        welcome_text = f"Thank you for calling {hotel_name}. How can I assist you today?"
        
        encoded_text = urllib.parse.quote(welcome_text)
        
        # Gather speech input
        gather = Gather(input="speech", action="/handle-speech", speechTimeout="auto")
        gather.play(f"/speak?text={encoded_text}")
        
        response.append(gather)
        
        # If no input, end call or redirect
        response.say("I didn't hear anything. Goodbye.")
        
        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        logger.error(f"Error in /incoming-call: {str(e)}")
        # Return a fallback XML response
        response = VoiceResponse()
        response.say("We are currently experiencing technical difficulties. Please try again later.")
        return Response(content=str(response), media_type="application/xml")

@app.post("/handle-speech")
async def handle_speech(request: Request, SpeechResult: str = Form(None)):
    """
    Handle speech input from Twilio Gather.
    """
    try:
        response = VoiceResponse()
        
        if SpeechResult:
            logger.info(f"Received speech: {SpeechResult}")
            # Get AI response
            ai_text = get_ai_response(SpeechResult)
            encoded_ai_text = urllib.parse.quote(ai_text)
            
            # Respond and listen again
            gather = Gather(input="speech", action="/handle-speech", speechTimeout="auto")
            gather.play(f"/speak?text={encoded_ai_text}")
            response.append(gather)
        else:
            # If speech result is empty
            response.say("I'm sorry, I didn't catch that. Could you please repeat?")
            response.redirect("/incoming-call") # Restart loop or handle differently

        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        logger.error(f"Error in /handle-speech: {str(e)}")
        response = VoiceResponse()
        response.say("An error occurred. Goodbye.")
        return Response(content=str(response), media_type="application/xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
