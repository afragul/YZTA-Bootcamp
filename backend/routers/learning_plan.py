import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.api_contract import CVUploadResponse, LearningPlanRequest, LearningPlanResponse
from services.learning_plan_service import LearningPlanError, create_learning_plan

logger = logging.getLogger(__name__)

router = APIRouter(tags=["learning-plan"])


@router.post("/learning-plan", response_model=LearningPlanResponse)
def generate_learning_plan(
    payload: LearningPlanRequest,
    db: Session = Depends(get_db),
) -> LearningPlanResponse:
    """Hedef role gore ogrenme plani uretir (Kisi 3 LearningPathService)."""
    try:
        return create_learning_plan(
            db,
            cv_id=payload.cv_id,
            target_role=payload.target_role,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except LearningPlanError as exc:
        logger.exception("learning_plan failed cv_id=%s", payload.cv_id)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
