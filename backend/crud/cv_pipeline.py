import json

from sqlalchemy.orm import Session

from models.analysis import Analysis
from models.cv import CV
from models.job_match import JobMatch
from models.learning_plan import LearningPlan
from schemas.api_contract import CVUploadResponse, JobMatchItem
from schemas.cv_analysis import CVAnalysisOutput
from schemas.learning_plan import RankedRole
from services.learning_service import rank_roles


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
