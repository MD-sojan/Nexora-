# app/core/db.py
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
import asyncio

# ------------------------------
# Database Configuration
# ------------------------------

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://sojan:-gak5BcS7qfRuW$@sojan.fesc2uv.mongodb.net/")
DB_NAME = os.getenv("MONGO_DB", "defendix")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# Expose collections
users_collection = db["users"]
scans_collection = db["scans"]
reports_collection = db["reports"]
otp_collection = db["otp_codes"]
login_attempts_collection = db["login_attempts"]
refresh_tokens_collection = db["refresh_tokens"]

# ------------------------------
# Helpers
# ------------------------------

def fix_id(doc):
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

# ------------------------------
# Ensure TTL indexes for cleanup
# ------------------------------

async def ensure_indexes():
    await db.otp_codes.create_index("expires", expireAfterSeconds=0)
    await db.login_attempts.create_index("time", expireAfterSeconds=900)  # 15 minutes
    await db.refresh_tokens.create_index("created_at", expireAfterSeconds=60*60*24*7)  # 7 days

# Run index creation at startup
async def init_db():
    await ensure_indexes()
