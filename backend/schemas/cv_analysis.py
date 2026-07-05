from pydantic import BaseModel, Field


class EducationItem(BaseModel):
    degree: str = Field(description="Derece/Diploma (orn: Lisans, Yuksek Lisans)")
    school: str = Field(description="Okul/Universite adi")
    department: str = Field(description="Bolum adi")
    graduation_year: int = Field(description="Mezuniyet yili")


class RoleScores(BaseModel):
    backend_developer: int = Field(default=0, ge=0, le=100)
    frontend_developer: int = Field(default=0, ge=0, le=100)
    machine_learning_engineer: int = Field(default=0, ge=0, le=100)
    data_scientist: int = Field(default=0, ge=0, le=100)
    devops_engineer: int = Field(default=0, ge=0, le=100)


class CVAnalysisOutput(BaseModel):
    """Kisi 2 (CV Analiz) cikti semasi - ekip kontrati."""

    skills: list[str]
    experience_years: float
    education: list[EducationItem]
    strengths: list[str]
    gaps: list[str]
    role_scores: RoleScores
