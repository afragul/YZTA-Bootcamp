import json
import uuid

from sqlalchemy.orm import Session

from models.analysis import Analysis
from models.cv import CV
from models.job_match import JobMatch
from schemas.api_contract import CVUploadResponse, JobMatchItem
from schemas.cv_analysis import CVAnalysisOutput


def create_cv_record(
    db: Session,
    *,
    filename: str,
    file_path: str,
    raw_text: str,
    user_id: int | None = None,
) -> CV:
    cv = CV(
        public_id=str(uuid.uuid4()),
        user_id=user_id,
        filename=filename,
        file_path=file_path,
        raw_text=raw_text,
    )
    db.add(cv)
    db.commit()
    db.refresh(cv)
    return cv


def save_analysis_and_matches(
    db: Session,
    *,
    cv: CV,
    analysis_data: dict,
    top_matches: list[dict],
) -> Analysis:
    analysis = Analysis(
        cv_id=cv.id,
        skills_json=json.dumps(analysis_data.get("skills", []), ensure_ascii=False),
        experience_years=float(analysis_data.get("experience_years", 0)),
        education_json=json.dumps(analysis_data.get("education", []), ensure_ascii=False),
        strengths_json=json.dumps(analysis_data.get("strengths", []), ensure_ascii=False),
        gaps_json=json.dumps(analysis_data.get("gaps", []), ensure_ascii=False),
        role_scores_json=json.dumps(analysis_data.get("role_scores", {}), ensure_ascii=False),
        top_role_reasons_json=json.dumps(
            analysis_data.get("top_role_reasons", []), ensure_ascii=False
        ),
    )
    db.add(analysis)
    db.flush()

    for idx, match in enumerate(top_matches):
        db.add(
            JobMatch(
                analysis_id=analysis.id,
                job_id=str(idx + 1),
                title=match["title"],
                job_domain=match["job_domain"],
                work_type=match["work_type"],
                job_location=match["job_location"],
                match_percent=float(match["match_percent"]),
                description=match["description"],
            )
        )

    db.commit()
    db.refresh(analysis)
    return analysis


def build_upload_response(
    cv: CV,
    analysis_data: dict,
    top_matches: list[dict],
    message: str,
) -> CVUploadResponse:
    return CVUploadResponse(
        cv_id=cv.public_id,
        filename=cv.filename,
        status="completed",
        message=message,
        analysis=CVAnalysisOutput(**analysis_data),
        top_matches=[JobMatchItem(**m) for m in top_matches],
    )
