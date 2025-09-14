from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, analyze, auth
from app.core.db import init_db

# Initialize FastAPI
app = FastAPI(title="Nexora Backend", version="1.0.0")

# Connect to MongoDB


# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Replace "*" with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(chat.router, prefix="/api", tags=["Chat"]) # Gemini Chat
app.include_router(analyze.router, prefix="/api", tags=["Analyzer"]) # Malware/Phishing Analyzer
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"]) # Authentication (signup/login/profile)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Nexora Backend is running!"}

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}
