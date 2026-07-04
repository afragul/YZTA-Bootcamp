from uuid import uuid4

from fastapi import APIRouter, File, UploadFile

from schemas.api_contract import CVUploadResponse
from services.mock_responses import build_mock_upload_response

router = APIRouter(prefix="/cv", tags=["cv"])


@router.post("/upload", response_model=CVUploadResponse)
async def upload_cv(file: UploadFile = File(...)) -> CVUploadResponse:
    """Hafta 1 mock endpoint.

    Gercek dosya isleme Hafta 2'de eklenecek.
    Simdilik ekip entegrasyonu icin sabit mock JSON doner.
    """
    await file.read()
    return build_mock_upload_response(cv_id=str(uuid4()), filename=file.filename or "cv.pdf")
