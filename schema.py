from pydantic import BaseModel, Field
from typing import List, Dict

class EducationItem(BaseModel):
    degree: str = Field(description="Derece/Diploma (örn: Lisans, Yüksek Lisans)")
    school: str = Field(description="Okul/Üniversite adı")
    department: str = Field(description="Bölüm adı")
    graduation_year: int = Field(description="Mezuniyet yılı")

class CVAnalysisOutput(BaseModel):
    skills: List[str] = Field(description="Adayın sahip olduğu teknik beceriler ve araçlar")
    experience_years: float = Field(description="Toplam iş deneyimi (yıl bazında)")
    education: List[EducationItem] = Field(description="Eğitim bilgileri listesi")
    strengths: List[str] = Field(description="CV'deki güçlü yönler ve öne çıkan başarılar")
    gaps: List[str] = Field(description="Hedef rollere göre eksik beceriler veya gelişim alanları")
    role_scores: Dict[str, int] = Field(
        description="Belirlenen her hedef rol için 0-100 arası uygunluk skoru"
    )
