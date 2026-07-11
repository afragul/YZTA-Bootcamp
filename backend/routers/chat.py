"""
Chat router

- POST /chat/session : analiz + eslesen ilanlardan koc oturumu acar
- POST /chat         : mesaj gonderip koc cevabi alir (contract: ChatRequest/Response).
"""
from fastapi import APIRouter, HTTPException

from schemas.api_contract import (
    ChatRequest,
    ChatResponse,
    ChatSessionInitRequest,
    ChatSessionInitResponse,
)
from services.coach_service import get_coach

router = APIRouter(tags=["chat"])


@router.post("/chat/session", response_model=ChatSessionInitResponse)
async def init_chat_session(payload: ChatSessionInitRequest) -> ChatSessionInitResponse:
    """CV analizi + eslesen ilanlarla yeni bir koc oturumu baslatir."""
    try:
        coach = get_coach()
        session_id = coach.create_session(payload.analysis, payload.top_matches)
        return ChatSessionInitResponse(session_id=session_id)
    except ValueError as e:  # orn. GEMINI_API_KEY yok
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    """Koca mesaj gonderir. session_id yoksa baglamsiz genel oturum acilir."""
    try:
        coach = get_coach()
        reply, session_id = coach.chat(payload.message, payload.session_id)
        return ChatResponse(reply=reply, session_id=session_id)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:  # noqa: BLE001 - LLM cagrisi patlarsa 502 don
        raise HTTPException(status_code=502, detail=f"Koc cevabi alinamadi: {e}")