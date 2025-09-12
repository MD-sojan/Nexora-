from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, analyze

app = FastAPI(title="Nexora Backend", version="1.0.0")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ For production, replace "*" with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(chat.router, prefix="/api", tags=["Chat"])      # Gemini Chat
app.include_router(analyze.router, prefix="/api", tags=["Analyzer"])  # Malware/Phishing Analyzer

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Nexora Backend is running with Gemini!"}
