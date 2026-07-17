from enum import Enum

from pydantic import BaseModel, Field


class TargetRole(str, Enum):

    # Yazilim gelistirme
    BACKEND_DEVELOPER = "backend_developer"
    FRONTEND_DEVELOPER = "frontend_developer"
    FULLSTACK_DEVELOPER = "fullstack_developer"
    MOBILE_DEVELOPER = "mobile_developer"
    DEVOPS_ENGINEER = "devops_engineer"
    CLOUD_ENGINEER = "cloud_engineer"

    # Yapay zeka ve veri
    MACHINE_LEARNING_ENGINEER = "machine_learning_engineer"
    DATA_SCIENTIST = "data_scientist"
    DATA_ENGINEER = "data_engineer"
    DATA_ANALYST = "data_analyst"
    BI_ANALYST = "bi_analyst"
    DATABASE_ADMINISTRATOR = "database_administrator"

    # Guvenlik ve sistem
    CYBERSECURITY_SPECIALIST = "cybersecurity_specialist"
    SYSTEMS_ADMINISTRATOR = "systems_administrator"

    # Tasarim
    UI_UX_DESIGNER = "ui_ux_designer"
    GRAPHIC_DESIGNER = "graphic_designer"

    # Urun ve yonetim
    PRODUCT_MANAGER = "product_manager"
    PROJECT_MANAGER = "project_manager"
    BUSINESS_ANALYST = "business_analyst"

    # Pazarlama, IK, musteri
    DIGITAL_MARKETING_SPECIALIST = "digital_marketing_specialist"
    HR_SPECIALIST = "hr_specialist"
    CUSTOMER_SUCCESS_SPECIALIST = "customer_success_specialist"


class LearningStep(BaseModel):
    """Ogrenme planindaki tek bir adim."""

    order: int = Field(description="Hafta icindeki adim sirasi (1, 2, 3...)")
    topic: str = Field(
        description="Ogrenilecek konu. Orn: 'Docker temelleri' veya "
                    "'Ise alim gorusme teknikleri'"
    )
    reason: str = Field(
        description="Bu adim NEDEN gerekli. Adayin hangi eksigini kapatiyor ve "
                    "hedef rolde ne ise yariyor."
    )
    resource_type: str = Field(
        description="Kaynak turu: kurs | dokumantasyon | video | kitap | proje"
    )
    resource_suggestion: str = Field(
        description="SOMUT kaynak onerisi. Orn: 'Docker resmi dokumantasyonu - "
                    "Get Started' veya 'Figma Community'den bir dashboard klonla'. "
                    "'Bir kurs al' gibi bos oneri YASAK."
    )
    estimated_hours: int = Field(description="Bu adim icin tahmini calisma saati")


class WeeklyPlan(BaseModel):
    """Bir haftalik plan."""

    week: int = Field(description="Hafta numarasi (1, 2, 3...)")
    focus: str = Field(description="Bu haftanin ana odagi, tek cumle")
    steps: list[LearningStep] = Field(description="Bu haftanin adimlari (2-4 adim)")


class LearningPlanOutput(BaseModel):
    """
    Ogrenme Yolu Agent'inin cikti semasi
    Gemini bu semaya uygun JSON uretir.
    """

    target_role: str = Field(description="Plan hangi rol icin uretildi")
    summary: str = Field(
        description="Planin 2-3 cumlelik ozeti: adayin mevcut durumu ve bu planin "
                    "onu nereye goturecegi."
    )
    total_weeks: int = Field(description="Planin toplam hafta sayisi")
    weeks: list[WeeklyPlan] = Field(description="Haftalik planlar")


class RankedRole(BaseModel):
    """
    Bir rolun, adayin skoruna gore siralanmis hali.
    Frontend rol secicisi ve otomatik plan bunu kullanir.
    """

    rank: int = Field(description="Siralama (1 = adaya en uygun rol)")
    role: str = Field(description="Teknik rol adi (TargetRole degeri)")
    display: str = Field(description="Kullaniciya gosterilecek ad")
    score: int = Field(ge=0, le=100, description="Adayin bu roldeki uygunluk skoru")
    auto: bool = Field(
        description="True ise dashboard acilinca plani OTOMATIK uretilir (sadece "
                    "rank=1). Diger 21 rol butona basilinca uretilir."
    )