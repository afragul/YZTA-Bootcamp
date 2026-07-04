from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class JobMatch(Base):
    __tablename__ = "job_matches"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    analysis_id: Mapped[int] = mapped_column(ForeignKey("analyses.id"))
    job_id: Mapped[str] = mapped_column(String(64))
    title: Mapped[str] = mapped_column(String(255))
    job_domain: Mapped[str] = mapped_column(String(128))
    work_type: Mapped[str] = mapped_column(String(64))
    job_location: Mapped[str] = mapped_column(String(128))
    match_percent: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(Text)

    analysis: Mapped["Analysis"] = relationship(back_populates="job_matches")
