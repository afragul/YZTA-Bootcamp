from pydantic import BaseModel, Field
from typing import List

class EducationItem(BaseModel):
    degree: str = Field(description="Derece/Diploma (örn: Lisans, Yüksek Lisans)")
    school: str = Field(description="Okul/Üniversite adı")
    department: str = Field(description="Bölüm adı")
    graduation_year: int = Field(description="Mezuniyet yılı")

class RoleScores(BaseModel):
    backend_developer: int = Field(default=0, description="Backend Developer uygunluk skoru (0-100)")
    frontend_developer: int = Field(default=0, description="Frontend Developer uygunluk skoru (0-100)")
    machine_learning_engineer: int = Field(default=0, description="Machine Learning Engineer uygunluk skoru (0-100)")
    data_scientist: int = Field(default=0, description="Data Scientist uygunluk skoru (0-100)")
    devops_engineer: int = Field(default=0, description="DevOps Engineer uygunluk skoru (0-100)")

class CVAnalysisOutput(BaseModel):
    skills: List[str] = Field(description="Adayın sahip olduğu teknik beceriler ve araçlar")
    experience_years: float = Field(description="Toplam iş deneyimi (yıl bazında)")
    education: List[EducationItem] = Field(description="Eğitim bilgileri listesi")
    strengths: List[str] = Field(description="CV'deki güçlü yönler ve öne çıkan başarılar")
    gaps: List[str] = Field(description="Hedef rollere göre eksik beceriler veya gelişim alanları")
    role_scores: RoleScores = Field(
        description="Belirlenen her hedef rol için 0-100 arası uygunluk skoru nesnesi"
    )
