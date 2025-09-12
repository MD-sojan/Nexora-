import json
from fastapi import APIRouter, HTTPException, Form, Body, Depends, status
from fastapi.responses import StreamingResponse
from typing import Optional, Annotated
from app.services.gpt_service import ask_gpt_stream
from app.services import auth_service
from app.models.auth import UserInDB

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(
    current_user: Annotated[UserInDB, Depends(auth_service.get_current_user)],
    message: Optional[str] = Form(None),
    prompt: Optional[str] = Form(None),
    data: Optional[str] = Form("{}"),
    body: dict = Body(None)  # also accept JSON body
):
    """
    Chat endpoint with streaming response.
    Returns structured JSON events for each chunk.
    Supports both Form-data and JSON input.
    """
    # Determine input text
    if body and isinstance(body, dict):
        text = body.get("message") or body.get("prompt")
        extra_data = body.get("data", {})
        if isinstance(extra_data, str):
            try:
                extra_data = json.loads(extra_data)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON in 'data'")
    else:
        text = message or prompt
        try:
            extra_data = json.loads(data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON in 'data'")
    if not text:
        raise HTTPException(status_code=400, detail="No message provided")

    # Stream structured response
    try:
        gpt_generator = ask_gpt_stream(text, extra_data=extra_data)
        return StreamingResponse(
            format_stream(current_user.username, text, gpt_generator, extra_data),
            media_type="text/event-stream"
        )
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"GPT call failed: {str(e)}")


