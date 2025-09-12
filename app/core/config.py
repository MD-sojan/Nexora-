import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEXORA_GPT_MODEL = os.getenv("NEXORA_GPT_MODEL", "gpt-4o-mini")

# --- NEW AUTHENTICATION CONFIG ---
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-replace-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
