import os
from elevenlabs import ElevenLabs

def generate_speech(text: str):
    """
    Generates audio from text using ElevenLabs.
    Returns an iterator of bytes (audio stream).
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("Warning: ELEVENLABS_API_KEY not set")
        return None

    client = ElevenLabs(api_key=api_key)
    
    # Generate audio
    # using a popular pre-made voice
    audio = client.generate(
        text=text,
        voice="Rachel", 
        model="eleven_monolingual_v1"
    )
    return audio

