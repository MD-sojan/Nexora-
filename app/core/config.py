import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEXORA_GPT_MODEL = os.getenv("NEXORA_GPT_MODEL", "gpt-5")
