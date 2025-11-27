# Hotel Agent

This is an AI agent built with:
- **Render**: For hosting and deployment.
- **GitHub**: For version control and CI/CD.
- **Twilio**: For handling incoming calls and SMS.
- **ElevenLabs**: For realistic voice generation.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env`:
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `ELEVENLABS_API_KEY`
   - `OPENAI_API_KEY` (if using LLM for logic)

3. Run locally:
   ```bash
   uvicorn main:app --reload
   ```

