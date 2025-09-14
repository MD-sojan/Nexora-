from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.services.auth_service import (
 get_password_hash,
 verify_password,
 create_access_token,
 find_user_by_username,
 get_current_user
)
from app.core.db import users_collection
from app.models.auth import User, UserInDB, Token, UserCreate

router = APIRouter()

# --- Signup ---
@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
async def signup(user_create: UserCreate):
    existing_user = await find_user_by_username(user_create.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check if email already exists
    existing_email = await users_collection.find_one({"email": user_create.email})
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
 
    hashed_password = get_password_hash(user_create.password)
    user_doc = {
        "username": user_create.username,
        "email": user_create.email,
        "hashed_password": hashed_password
    }
    await users_collection.insert_one(user_doc)
    return User(**user_doc) # Return the user without the hashed password

# --- Login ---
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await find_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- Profile ---
@router.get("/me", response_model=User)
async def read_profile(current_user: UserInDB = Depends(get_current_user)):
    """
    Returns the profile info of the currently logged-in user.
    Only username and email are exposed.
    """
    return current_user # Pydantic will automatically exclude hashed_password
