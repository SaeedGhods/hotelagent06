import os
from openai import OpenAI

def get_ai_response(user_input: str, system_prompt: str = None) -> str:
    """
    Get a response from OpenAI based on user input and system configuration.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not set")
        return "I am sorry, but I am not configured correctly."

    try:
        # Initialize client lazily to avoid startup crashes
        client = OpenAI(api_key=api_key)
        
        # Default system prompt if none provided
        if not system_prompt:
            hotel_name = os.getenv("HOTEL_NAME", "Grand Hotel")
            system_prompt = f"""You are a helpful and polite concierge at {hotel_name}. 
            Keep your responses concise (1-2 sentences) because you are speaking over the phone.
            Do not use markdown or special characters.
            If asked about room availability, say you can check that.
            """

        response = client.chat.completions.create(
            model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return "I apologize, but I'm having trouble connecting to my brain right now. Please try again later."
