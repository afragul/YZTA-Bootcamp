from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cv_id: Mapped[int] = mapped_column(ForeignKey("cvs.id"))
    skills_json: Mapped[str] = mapped_column(Text)
    experience_years: Mapped[float] = mapped_column(Float)
    education_json: Mapped[str] = mapped_column(Text)
    strengths_json: Mapped[str] = mapped_column(Text)
    gaps_json: Mapped[str] = mapped_column(Text)
    role_scores_json: Mapped[str] = mapped_column(Text)
    top_role_reasons_json: Mapped[str] = mapped_column(Text, default="[]")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    cv: Mapped["CV"] = relationship(back_populates="analyses")
    job_matches: Mapped[list["JobMatch"]] = relationship(back_populates="analysis")
    learning_plans: Mapped[list["LearningPlan"]] = relationship(back_populates="analysis")
