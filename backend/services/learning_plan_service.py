import json
import logging

from sqlalchemy.orm import Session

from crud import cv_pipeline
from schemas.api_contract import LearningPlanResponse
from schemas.learning_plan import LearningPlanOutput
from services.learning_service import LearningPathService

logger = logging.getLogger(__name__)


class LearningPlanError(Exception):
    """Ogrenme plani uretimi basarisiz."""


def create_learning_plan(
    db: Session,
    *,
    cv_id: str,
    target_role: str,
) -> LearningPlanResponse:
    cv = cv_pipeline.get_cv_by_public_id(db, cv_id)
    if not cv:
        raise ValueError(f"CV bulunamadi: {cv_id}")

    analysis = cv_pipeline.get_latest_analysis(db, cv)
    if not analysis:
        raise ValueError("Bu CV icin analiz bulunamadi. Once /cv/upload calistirin.")

    cached = cv_pipeline.get_learning_plan(db, analysis.id, target_role)
    if cached:
        logger.info("learning_plan cache hit cv_id=%s role=%s", cv_id, target_role)
        plan_data = json.loads(cached.plan_json)
        return LearningPlanResponse(
            cv_id=cv_id,
            target_role=target_role,
            cached=True,
            plan=LearningPlanOutput(**plan_data),
        )

    analysis_data = cv_pipeline.analysis_to_dict(analysis)
    gaps = cv_pipeline.gaps_for_target_role(analysis_data["gaps"], target_role)
    skills = analysis_data["skills"]

    logger.info(
        "learning_plan generating cv_id=%s role=%s gaps=%d skills=%d",
        cv_id,
        target_role,
        len(gaps),
        len(skills),
    )

    service = LearningPathService()
    try:
        plan_data = service.build_plan(target_role, gaps, skills)
    except ValueError:
        raise
    except Exception as exc:
        raise LearningPlanError(f"Ogrenme plani uretilemedi: {exc}") from exc

    cv_pipeline.save_learning_plan(
        db,
        analysis_id=analysis.id,
        target_role=target_role,
        plan_data=plan_data,
    )

    return LearningPlanResponse(
        cv_id=cv_id,
        target_role=target_role,
        cached=False,
        plan=LearningPlanOutput(**plan_data),
    )
