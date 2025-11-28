import os
import sys

# DEBUG: Check installed packages without pkg_resources to avoid missing dep error
try:
    import importlib.metadata
    version = importlib.metadata.version("elevenlabs")
    print(f"DEBUG: Installed elevenlabs version: {version}")
except Exception as e:
    print(f"DEBUG: Could not determine elevenlabs version: {e}")

# Try to handle ALL potential import styles because Render's environment is unpredictable
try:
    # V1.0+ Client Style
    from elevenlabs.client import ElevenLabs
    HAS_CLIENT = True
    print("DEBUG: Imported ElevenLabs client successfully")
except ImportError:
    HAS_CLIENT = False
    print("DEBUG: Could not import elevenlabs.client.ElevenLabs")

try:
    # Legacy Style
    from elevenlabs import generate, set_api_key
    HAS_LEGACY = True
    print("DEBUG: Imported legacy generate/set_api_key successfully")
except ImportError:
    HAS_LEGACY = False
    print("DEBUG: Could not import legacy elevenlabs functions")


def generate_speech(text: str):
    """
    Generates audio from text using ElevenLabs.
    Returns an iterator of bytes (audio stream).
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("Warning: ELEVENLABS_API_KEY not set")
        return None

    voice_id = os.getenv("ELEVENLABS_VOICE_ID", "Rachel")

    # STRATEGY 1: Use V1.0+ Client
    if HAS_CLIENT:
        try:
            print(f"DEBUG: Using V1 Client for {voice_id}")
            client = ElevenLabs(api_key=api_key)
            audio = client.generate(
                text=text,
                voice=voice_id, 
                model="eleven_monolingual_v1"
            )
            return audio
        except Exception as e:
            print(f"DEBUG: V1 Client execution failed: {e}")
            # Do not return yet, try legacy as fallback if available

    # STRATEGY 2: Use Legacy
    if HAS_LEGACY:
        try:
            print(f"DEBUG: Using Legacy Generate for {voice_id}")
            set_api_key(api_key)
            audio = generate(
                text=text,
                voice=voice_id,
                model="eleven_monolingual_v1"
            )
            return audio
        except Exception as e:
            print(f"DEBUG: Legacy execution failed: {e}")
    
    print("ERROR: All ElevenLabs generation methods failed.")
    return None
