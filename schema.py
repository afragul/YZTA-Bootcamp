from pydantic import BaseModel, Field
from typing import List

class EducationItem(BaseModel):
    degree: str = Field(description="Derece/Diploma (örn: Lisans, Yüksek Lisans)")
    school: str = Field(description="Okul/Üniversite adı")
    department: str = Field(description="Bölüm adı")
    graduation_year: int = Field(description="Mezuniyet yılı")

class RoleScores(BaseModel):
    # Teknoloji & Yazılım Geliştirme (Software Engineering)
    backend_developer: int = Field(default=0, description="Backend Developer uygunluk skoru (0-100)")
    frontend_developer: int = Field(default=0, description="Frontend Developer uygunluk skoru (0-100)")
    fullstack_developer: int = Field(default=0, description="Full Stack Developer uygunluk skoru (0-100)")
    mobile_developer: int = Field(default=0, description="Mobile Developer uygunluk skoru (0-100)")
    devops_engineer: int = Field(default=0, description="DevOps Engineer uygunluk skoru (0-100)")
    cloud_engineer: int = Field(default=0, description="Cloud Engineer / Architect uygunluk skoru (0-100)")
    
    # Yapay Zeka & Veri Sistemleri (AI & Data Systems)
    machine_learning_engineer: int = Field(default=0, description="Machine Learning Engineer uygunluk skoru (0-100)")
    data_scientist: int = Field(default=0, description="Data Scientist uygunluk skoru (0-100)")
    data_engineer: int = Field(default=0, description="Data Engineer uygunluk skoru (0-100)")
    data_analyst: int = Field(default=0, description="Data Analyst uygunluk skoru (0-100)")
    bi_analyst: int = Field(default=0, description="Business Intelligence (BI) Analyst uygunluk skoru (0-100)")
    database_administrator: int = Field(default=0, description="Database Administrator (DBA) uygunluk skoru (0-100)")
    
    # Güvenlik, Sistem & Ağ (Security & Infrastructure)
    cybersecurity_specialist: int = Field(default=0, description="Cybersecurity Specialist / Analyst uygunluk skoru (0-100)")
    systems_administrator: int = Field(default=0, description="Systems / Network Administrator uygunluk skoru (0-100)")
    
    # Tasarım & Yaratıcı (Design & Creative)
    ui_ux_designer: int = Field(default=0, description="UI/UX Designer uygunluk skoru (0-100)")
    graphic_designer: int = Field(default=0, description="Graphic Designer uygunluk skoru (0-100)")
    
    # Ürün, Yönetim & Analiz (Product, Management & Business Analysis)
    product_manager: int = Field(default=0, description="Product Manager / Product Owner uygunluk skoru (0-100)")
    project_manager: int = Field(default=0, description="Project Manager / Scrum Master uygunluk skoru (0-100)")
    business_analyst: int = Field(default=0, description="Business Analyst uygunluk skoru (0-100)")
    
    # Pazarlama, İK & Müşteri İlişkileri (Business Ops & HR)
    digital_marketing_specialist: int = Field(default=0, description="Digital Marketing Specialist uygunluk skoru (0-100)")
    hr_specialist: int = Field(default=0, description="HR Specialist / Recruiter uygunluk skoru (0-100)")
    customer_success_specialist: int = Field(default=0, description="Customer Success Specialist / Manager uygunluk skoru (0-100)")

class CVAnalysisOutput(BaseModel):
    skills: List[str] = Field(description="Adayın sahip olduğu teknik ve sosyal beceriler")
    experience_years: float = Field(description="Toplam iş deneyimi (yıl bazında)")
    education: List[EducationItem] = Field(description="Eğitim bilgileri listesi")
    strengths: List[str] = Field(description="CV'deki güçlü yönler ve öne çıkan başarılar")
    gaps: List[str] = Field(description="Hedef rollere göre eksik beceriler veya gelişim alanları")
    role_scores: RoleScores = Field(
        description="Belirlenen her hedef rol için 0-100 arası uygunluk skoru nesnesi"
    )
