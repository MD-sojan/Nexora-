


from fastapi import APIRouter, UploadFile, HTTPException
from app.services.analyzer import analyze_file
import traceback

router = APIRouter()

@router.post("/analyze")
async def analyze(file: UploadFile):
    """Run static analyzer on uploaded file."""
    try:
        result = await analyze_file(file)
        return result
    except Exception as e:
        # Capture full traceback for debugging
        error_details = traceback.format_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Analyzer failed: {str(e)}\n{error_details}"
        )
