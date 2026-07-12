from pydantic import BaseModel, Field


class EducationItem(BaseModel):
    degree: str = Field(description="Derece/Diploma (orn: Lisans, Yuksek Lisans)")
    school: str = Field(description="Okul/Universite adi")
    department: str = Field(description="Bolum adi")
    graduation_year: int = Field(description="Mezuniyet yili")

class RoleReason(BaseModel):
    """En yuksek skorlu roller icin kisa gerekce - Kisi 3 (Rol Skorlama)."""

    role: str = Field(
        description="Rolun teknik adi. role_scores icindeki alan adiyla AYNI olmali "
                    "(orn: machine_learning_engineer)"
    )
    score: int = Field(ge=0, le=100, description="role_scores icindeki ayni skor")
    reason: str = Field(
        description="Bu skorun 1-2 cumlelik gerekcesi. CV'den SOMUT kanit gosterilmeli."
    )


class RoleScores(BaseModel):
    # Teknoloji & Yazılım Geliştirme (Software Engineering)
    backend_developer: int = Field(default=0, ge=0, le=100)
    frontend_developer: int = Field(default=0, ge=0, le=100)
    fullstack_developer: int = Field(default=0, ge=0, le=100)
    mobile_developer: int = Field(default=0, ge=0, le=100)
    devops_engineer: int = Field(default=0, ge=0, le=100)
    cloud_engineer: int = Field(default=0, ge=0, le=100)
    
    # Yapay Zeka & Veri Sistemleri (AI & Data Systems)
    machine_learning_engineer: int = Field(default=0, ge=0, le=100)
    data_scientist: int = Field(default=0, ge=0, le=100)
    data_engineer: int = Field(default=0, ge=0, le=100)
    data_analyst: int = Field(default=0, ge=0, le=100)
    bi_analyst: int = Field(default=0, ge=0, le=100)
    database_administrator: int = Field(default=0, ge=0, le=100)
    
    # Güvenlik, Sistem & Ağ (Security & Infrastructure)
    cybersecurity_specialist: int = Field(default=0, ge=0, le=100)
    systems_administrator: int = Field(default=0, ge=0, le=100)
    
    # Tasarım & Yaratıcı (Design & Creative)
    ui_ux_designer: int = Field(default=0, ge=0, le=100)
    graphic_designer: int = Field(default=0, ge=0, le=100)
    
    # Ürün, Yönetim & Analiz (Product, Management & Business Analysis)
    product_manager: int = Field(default=0, ge=0, le=100)
    project_manager: int = Field(default=0, ge=0, le=100)
    business_analyst: int = Field(default=0, ge=0, le=100)
    
    # Pazarlama, İK & Müşteri İlişkileri (Business Ops & HR)
    digital_marketing_specialist: int = Field(default=0, ge=0, le=100)
    hr_specialist: int = Field(default=0, ge=0, le=100)
    customer_success_specialist: int = Field(default=0, ge=0, le=100)


class CVAnalysisOutput(BaseModel):
    """Kisi 2 (CV Analiz) cikti semasi - ekip kontrati."""

    skills: list[str]
    experience_years: float
    education: list[EducationItem]
    strengths: list[str]
    gaps: list[str]
    role_scores: RoleScores
    top_role_reasons: list[RoleReason] = Field(
        description="role_scores icinde EN YUKSEK skora sahip 3 rol. "
                    "Skora gore azalan sirada siralanmali."
    )
