from pydantic import BaseModel, Field

from schemas.cv_analysis import CVAnalysisOutput


class HealthResponse(BaseModel):
    status: str
    service: str


class JobMatchItem(BaseModel):
    """Kisi 4 (RAG) top_matches[] ogesi - ekip kontrati."""

    title: str
    job_domain: str
    work_type: str
    job_location: str
    match_percent: float = Field(ge=0, le=100)
    description: str


class CVUploadResponse(BaseModel):
    """POST /cv/upload mock cevabi (Hafta 1).

    Hafta 3 orkestrasyon endpoint'i ayni yapida tek JSON dondurur.
    """

    cv_id: str
    filename: str
    status: str = Field(description="uploaded | processing | completed")
    message: str
    analysis: CVAnalysisOutput
    top_matches: list[JobMatchItem]


# --- Gelecek endpoint kontratlari (Hafta 2+) ---


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    session_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    session_id: str


class ChatSessionInitRequest(BaseModel):
    """Orkestrasyon (Kisi 1) analiz + eslesmeyi verip koc oturumu acar."""

    analysis: CVAnalysisOutput
    top_matches: list[JobMatchItem]


class ChatSessionInitResponse(BaseModel):
    session_id: str