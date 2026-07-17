from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user_optional
from models.user import User
from schemas.api_contract import CVUploadResponse
from services.cv_parser import CVParseError
from services.cv_service import CVAnalysisError, InvalidCVError
from services.upload_service import process_cv_upload

router = APIRouter(prefix="/cv", tags=["cv"])


@router.post("/upload", response_model=CVUploadResponse)
async def upload_cv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
) -> CVUploadResponse:
    """Hafta 2: PDF/DOCX yukleme, parse, analiz ve RAG eslestirme."""
    file_bytes = await file.read()

    try:
        return process_cv_upload(
            db,
            file_bytes=file_bytes,
            filename=file.filename or "cv.pdf",
            content_type=file.content_type,
            user_id=current_user.id if current_user else None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except CVParseError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except InvalidCVError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    except CVAnalysisError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"CV isleme sirasinda beklenmeyen hata: {exc}",
        ) from exc
