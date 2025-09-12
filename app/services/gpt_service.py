import os
from openai import OpenAI
from app.core import config

# Initialize OpenAI client
client = OpenAI(api_key=config.OPENAI_API_KEY)

def ask_gpt(prompt: str) -> str:
    """Send prompt to OpenAI GPT model and return response."""
    response = client.chat.completions.create(
        model=config.NEXORA_GPT_MODEL,  # default: "gpt-5"
        messages=[
            {"role": "system", "content": "You are Nexora, a cybersecurity AI assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content

def ask_gpt_stream(prompt: str, model: str = config.NEXORA_GPT_MODEL):
    """
    Stream GPT response as a generator.
    """
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are Nexora AI, a helpful cybersecurity assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.3,
            stream=True  # <-- streaming mode
        )
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content
    except Exception as e:
        yield f"⚠️ Streaming failed: {str(e)}"
