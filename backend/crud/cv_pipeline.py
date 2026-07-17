import json
import uuid

from sqlalchemy.orm import Session

from models.analysis import Analysis
from models.cv import CV
from models.job_match import JobMatch
from models.learning_plan import LearningPlan
from schemas.api_contract import CVUploadResponse, JobMatchItem
from schemas.cv_analysis import CVAnalysisOutput
from schemas.learning_plan import RankedRole
from services.learning_service import rank_roles


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


def get_cv_by_public_id(db: Session, public_id: str) -> CV | None:
    return db.query(CV).filter(CV.public_id == public_id).first()


def get_latest_analysis(db: Session, cv: CV) -> Analysis | None:
    return (
        db.query(Analysis)
        .filter(Analysis.cv_id == cv.id)
        .order_by(Analysis.created_at.desc())
        .first()
    )


def analysis_to_dict(analysis: Analysis) -> dict:
    return {
        "skills": json.loads(analysis.skills_json),
        "experience_years": analysis.experience_years,
        "education": json.loads(analysis.education_json),
        "strengths": json.loads(analysis.strengths_json),
        "gaps": json.loads(analysis.gaps_json),
        "role_scores": json.loads(analysis.role_scores_json),
        "top_role_reasons": json.loads(analysis.top_role_reasons_json or "[]"),
    }


def get_job_matches(db: Session, analysis_id: int) -> list[dict]:
    rows = db.query(JobMatch).filter(JobMatch.analysis_id == analysis_id).all()
    return [
        {
            "title": row.title,
            "job_domain": row.job_domain,
            "work_type": row.work_type,
            "job_location": row.job_location,
            "match_percent": row.match_percent,
            "description": row.description,
        }
        for row in rows
    ]


def get_learning_plan(
    db: Session, analysis_id: int, target_role: str
) -> LearningPlan | None:
    return (
        db.query(LearningPlan)
        .filter(
            LearningPlan.analysis_id == analysis_id,
            LearningPlan.target_role == target_role,
        )
        .order_by(LearningPlan.created_at.desc())
        .first()
    )


def save_learning_plan(
    db: Session, *, analysis_id: int, target_role: str, plan_data: dict
) -> LearningPlan:
    record = LearningPlan(
        analysis_id=analysis_id,
        target_role=target_role,
        plan_json=json.dumps(plan_data, ensure_ascii=False),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def gaps_for_target_role(gaps: list[str], target_role: str) -> list[str]:
    """Hedef role etiketli gap maddelerini filtreler."""
    prefix = f"[{target_role}]"
    tagged = [g for g in gaps if g.strip().startswith(prefix)]
    if tagged:
        return [g[len(prefix) :].strip() for g in tagged]
    return gaps


def build_upload_response(
    cv: CV,
    analysis_data: dict,
    top_matches: list[dict],
    message: str,
) -> CVUploadResponse:
    rankings = rank_roles(analysis_data.get("role_scores", {}))
    return CVUploadResponse(
        cv_id=cv.public_id,
        filename=cv.filename,
        status="completed",
        message=message,
        analysis=CVAnalysisOutput(**analysis_data),
        top_matches=[JobMatchItem(**m) for m in top_matches],
        role_rankings=[RankedRole(**r) for r in rankings],
    )


def build_cv_detail_response(
    db: Session,
    cv: CV,
    analysis: Analysis,
    message: str = "CV analiz sonucu getirildi.",
) -> CVUploadResponse:
    analysis_data = analysis_to_dict(analysis)
    top_matches = get_job_matches(db, analysis.id)
    return build_upload_response(cv, analysis_data, top_matches, message)
