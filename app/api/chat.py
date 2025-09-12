import json
from fastapi import APIRouter, HTTPException, Form, Body
from fastapi.responses import StreamingResponse
from typing import Optional
from app.services.gpt_service import ask_gpt_stream

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(
    message: Optional[str] = Form(None),
    prompt: Optional[str] = Form(None),
    data: Optional[str] = Form("{}"),
    body: dict = Body(None)  # also accept JSON body
):
    """
    Chat endpoint with streaming response.
    Supports both Form-data and JSON input.
    """
    # Check if request is JSON
    if body and isinstance(body, dict):
        text = body.get("message") or body.get("prompt")
        extra_data = body.get("data", {})
    else:
        # Fall back to form-data
        text = message or prompt
        try:
            extra_data = json.loads(data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON in 'data'")

    if not text:
        raise HTTPException(status_code=400, detail="No message provided")

    # Stream response
    try:
        return StreamingResponse(
            ask_gpt_stream(text),
            media_type="text/event-stream"  # use "text/plain" if frontend isn’t SSE ready
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GPT call failed: {str(e)}")
