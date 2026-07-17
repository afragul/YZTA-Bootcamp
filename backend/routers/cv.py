import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.api_contract import CVUploadResponse
from crud import cv_pipeline

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/cv", tags=["cv"])


@router.get("/{cv_id}", response_model=CVUploadResponse)
def get_cv_result(cv_id: str, db: Session = Depends(get_db)) -> CVUploadResponse:
    """Kayitli CV analiz sonucunu getirir (orkestrasyon ciktisi)."""
    cv = cv_pipeline.get_cv_by_public_id(db, cv_id)
    if not cv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CV bulunamadi.")

    analysis = cv_pipeline.get_latest_analysis(db, cv)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bu CV icin analiz bulunamadi.",
        )

    logger.info("cv result fetched public_id=%s", cv_id)
    return cv_pipeline.build_cv_detail_response(db, cv, analysis)
