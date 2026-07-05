from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class LearningPlan(Base):
    __tablename__ = "learning_plans"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    analysis_id: Mapped[int] = mapped_column(ForeignKey("analyses.id"))
    target_role: Mapped[str] = mapped_column(String(128))
    plan_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    analysis: Mapped["Analysis"] = relationship(back_populates="learning_plans")
