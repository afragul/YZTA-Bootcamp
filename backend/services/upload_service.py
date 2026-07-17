import os
from pathlib import Path
from uuid import uuid4

from sqlalchemy.orm import Session

from crud import cv_pipeline
from schemas.api_contract import CVUploadResponse
from services.cv_parser import extract_text
from services.cv_service import CVAnalysisService

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB

_current_dir = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(_current_dir, "..", "data", "uploads")


def _validate_upload(filename: str | None, content_type: str | None, size: int) -> str:
    if not filename:
        raise ValueError("Dosya adi gerekli.")

    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError("Sadece PDF ve DOCX dosyalari kabul edilir.")

    if size > MAX_FILE_SIZE_BYTES:
        raise ValueError("Dosya boyutu 5 MB sinirini asiyor.")

    if content_type:
        allowed_types = {
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }
        if content_type not in allowed_types:
            raise ValueError("Gecersiz dosya turu.")

    return suffix


def _save_file(data: bytes, suffix: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    stored_name = f"{uuid4()}{suffix}"
    file_path = os.path.join(UPLOAD_DIR, stored_name)
    with open(file_path, "wb") as f:
        f.write(data)
    return file_path


def process_cv_upload(
    db: Session,
    *,
    file_bytes: bytes,
    filename: str,
    content_type: str | None,
    user_id: int | None = None,
) -> CVUploadResponse:
    suffix = _validate_upload(filename, content_type, len(file_bytes))

    cv_text = extract_text(file_bytes, filename)
    file_path = _save_file(file_bytes, suffix)

    cv = cv_pipeline.create_cv_record(
        db,
        filename=filename,
        file_path=file_path,
        raw_text=cv_text,
        user_id=user_id,
    )

    analyzer = CVAnalysisService()
    analysis_data = analyzer.analyze_cv(cv_text)

    top_matches: list[dict] = []
    try:
        from services.search_jobs import search_jobs_from_analysis

        top_matches = search_jobs_from_analysis(analysis_data, n=5)
    except Exception:
        top_matches = []

    cv_pipeline.save_analysis_and_matches(
        db,
        cv=cv,
        analysis_data=analysis_data,
        top_matches=top_matches,
    )

    return cv_pipeline.build_upload_response(
        cv=cv,
        analysis_data=analysis_data,
        top_matches=top_matches,
        message="CV basariyla yuklendi, analiz edildi ve is ilanlari eslestirildi.",
    )


__all__ = [
    "ALLOWED_EXTENSIONS",
    "process_cv_upload",
]
