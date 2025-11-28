import os
import sys
import pkg_resources

# Debug: Print installed version immediately on import
try:
    version = pkg_resources.get_distribution("elevenlabs").version
    print(f"DEBUG: Installed elevenlabs version: {version}")
except Exception as e:
    print(f"DEBUG: Could not determine elevenlabs version: {e}")

try:
    from elevenlabs import ElevenLabs
    # Debug: Check what attributes exist on the class/module
    print(f"DEBUG: ElevenLabs attributes: {dir(ElevenLabs)}")
except ImportError:
    print("DEBUG: Could not import ElevenLabs from elevenlabs")

def generate_speech(text: str):
    """
    Generates audio from text using ElevenLabs.
    Returns an iterator of bytes (audio stream).
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("Warning: ELEVENLABS_API_KEY not set")
        return None

    try:
        # ATTEMPT 1: Try v1.x client style
        client = ElevenLabs(api_key=api_key)
        
        voice_id = os.getenv("ELEVENLABS_VOICE_ID", "Rachel")
        
        print(f"DEBUG: Attempting client.generate with voice {voice_id}")
        audio = client.generate(
            text=text,
            voice=voice_id, 
            model="eleven_monolingual_v1"
        )
        return audio
        
    except Exception as e:
        print(f"DEBUG: v1.x client failed: {e}")
        
        # ATTEMPT 2: Fallback to v0.x style (static generate)
        # Some older versions use: from elevenlabs import generate
        try:
            from elevenlabs import generate, set_api_key
            set_api_key(api_key)
            print("DEBUG: Attempting legacy static generate()")
            audio = generate(
                text=text,
                voice=voice_id,
                model="eleven_monolingual_v1"
            )
            return audio
        except Exception as e2:
             print(f"DEBUG: Legacy generate failed too: {e2}")
             return None
