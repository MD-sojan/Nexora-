from fastapi import APIRouter, UploadFile, HTTPException, Depends, status
from app.services.analyzer import analyze_file
from app.models.analysis import AnalysisResult
import traceback
from app.services import auth_service
from app.models.auth import UserInDB
from typing import Annotated

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResult)
async def analyze(
    current_user: Annotated[UserInDB, Depends(auth_service.get_current_user)],
    file: UploadFile
):
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
