"""
AI Kariyer Kocu servisi

Gorev: Kullanicinin CV analizi + eslesen is ilanlarini bir RAG BAGLAMI'na
cevirip, bu baglam uzerinden konusan hafizali bir kariyer kocu saglamak.

Mimari not:
- Oturum hafizasi su an bellek-ici (in-memory). Demo icin yeterli; sunucu
  yeniden baslayinca sifirlanir. Kalicilik gerekirse ileride DB'ye tasinabilir
  (asagidaki _SESSIONS yerine bir tablo).
"""

import os
import uuid
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(override=True)

MODEL_NAME = "gemini-2.5-flash"

# role_scores alan adlari -> okunabilir etiket (baglamda sunmak icin)
_ROLE_LABELS: dict[str, str] = {
    "backend_developer": "Backend Developer",
    "frontend_developer": "Frontend Developer",
    "fullstack_developer": "Full Stack Developer",
    "mobile_developer": "Mobile Developer",
    "devops_engineer": "DevOps Engineer",
    "cloud_engineer": "Cloud Engineer",
    "machine_learning_engineer": "Machine Learning Engineer",
    "data_scientist": "Data Scientist",
    "data_engineer": "Data Engineer",
    "data_analyst": "Data Analyst",
    "bi_analyst": "BI Analyst",
    "database_administrator": "Database Administrator",
    "cybersecurity_specialist": "Cybersecurity Specialist",
    "systems_administrator": "Systems Administrator",
    "ui_ux_designer": "UI/UX Designer",
    "graphic_designer": "Graphic Designer",
    "product_manager": "Product Manager",
    "project_manager": "Project Manager",
    "business_analyst": "Business Analyst",
    "digital_marketing_specialist": "Digital Marketing Specialist",
    "hr_specialist": "HR Specialist",
    "customer_success_specialist": "Customer Success Specialist",
}

_SYSTEM_PERSONA = (
    "Sen NextGenCV uygulamasinin AI Kariyer Kocu'sun. Yazilim ve teknoloji "
    "alaninda kariyer hedefleyen adaylara yardim ediyorsun.\n\n"
    "KURALLAR:\n"
    "1. Sadece asagida VERILEN BAGLAM'a (adayin CV analizi + eslesen ilanlar) "
    "dayan. Baglamda olmayan bir sey uydurma; bilmiyorsan bilmedigini soyle.\n"
    "2. Somut, uygulanabilir ve tesvik edici ol. Genel gecer laf degil, adayin "
    "gucli yonlerine ve EKSIKLERINE (gaps) dogrudan deginen tavsiye ver.\n"
    "3. Ogrenme onerisi verirken adim adim ve onceliklendirilmis sekilde ver "
    "(once neyi ogrenmeli).\n"
    "4. Eslesen ilanlardan bahsederken uygunluk yuzdesine atif yapabilirsin.\n"
    "5. Turkce, samimi ama profesyonel bir dille, kisa ve net cevap ver.\n"
)


def _to_dict(obj: Any) -> dict:
    if obj is None:
        return {}
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if isinstance(obj, dict):
        return obj
    return dict(obj)


def _build_context(analysis: Any, top_matches: Any) -> str:
    """CV analizi + eslesen ilanlar -> LLM'e verilecek metinsel RAG baglami."""
    a = _to_dict(analysis)
    matches = [_to_dict(m) for m in (top_matches or [])]

    lines: list[str] = ["=== ADAY PROFILI (CV ANALIZI) ==="]

    skills = a.get("skills") or []
    if skills:
        lines.append(f"Beceriler: {', '.join(str(s) for s in skills)}")

    exp = a.get("experience_years")
    if exp is not None:
        lines.append(f"Deneyim: {exp} yil")

    strengths = a.get("strengths") or []
    if strengths:
        lines.append("Gucli yonler:")
        lines += [f"  - {s}" for s in strengths]

    gaps = a.get("gaps") or []
    if gaps:
        lines.append("Eksikler / gelisim alanlari:")
        lines += [f"  - {g}" for g in gaps]

    # En yuksek 5 rol skoru
    role_scores = a.get("role_scores") or {}
    role_scores = _to_dict(role_scores)
    if role_scores:
        top_roles = sorted(role_scores.items(), key=lambda kv: kv[1], reverse=True)[:5]
        lines.append("En uygun roller (0-100 uygunluk):")
        for field, score in top_roles:
            label = _ROLE_LABELS.get(field, field)
            lines.append(f"  - {label}: {score}")

    lines.append("")
    lines.append("=== EN UYGUN IS ILANLARI ===")
    if matches:
        for m in matches:
            pct = m.get("match_percent", "?")
            title = m.get("title", "Belirtilmemis")
            domain = m.get("job_domain", "-")
            wtype = m.get("work_type", "-")
            loc = m.get("job_location", "-")
            lines.append(f"  - %{pct} | {title} ({domain} / {wtype} / {loc})")
    else:
        lines.append("  (Henuz eslesen ilan yok.)")

    return "\n".join(lines)


class CareerCoachService:
    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY set edilmemis! .env dosyasini kontrol et."
            )
        self.client = genai.Client(api_key=api_key)
        # session_id -> {"context": str, "history": list[(role, text)]}
        self._sessions: dict[str, dict] = {}

    # --- Orkestrasyon (Kisi 1) bu kancayi cagirir ---
    def create_session(self, analysis: Any, top_matches: Any) -> str:
        """Analiz + eslesen ilanlardan RAG baglami kurup yeni oturum acar."""
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = {
            "context": _build_context(analysis, top_matches),
            "history": [],
        }
        return session_id

    def _ensure_session(self, session_id: str | None) -> str:
        """Gecerli oturum yoksa baglamsiz (genel) bir oturum ac."""
        if session_id and session_id in self._sessions:
            return session_id
        new_id = session_id or str(uuid.uuid4())
        self._sessions[new_id] = {
            "context": (
                "=== ADAY PROFILI ===\n(Henuz CV analiz edilmedi. Kisisellestirilmis "
                "tavsiye icin once CV yuklenip analiz edilmeli.)"
            ),
            "history": [],
        }
        return new_id

    # --- POST /chat bunu cagirir ---
    def chat(self, message: str, session_id: str | None = None) -> tuple[str, str]:
        """Bir mesaja koc cevabi uretir. (reply, session_id) doner."""
        sid = self._ensure_session(session_id)
        session = self._sessions[sid]

        system_instruction = _SYSTEM_PERSONA + "\n\n=== BAGLAM ===\n" + session["context"]

        # Gecmis + yeni mesaj -> google-genai 'contents' formati
        contents = []
        for role, text in session["history"]:
            contents.append({"role": role, "parts": [{"text": text}]})
        contents.append({"role": "user", "parts": [{"text": message}]})

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.6,
            ),
        )
        reply = (response.text or "").strip()

        # Hafizaya yaz (rol adlari: user / model)
        session["history"].append(("user", message))
        session["history"].append(("model", reply))
        return reply, sid


# Uygulama genelinde tek koc ornegi. Router bunu kullanir.
_coach: CareerCoachService | None = None

def get_coach() -> CareerCoachService:
    global _coach
    if _coach is None:
        _coach = CareerCoachService()
    return _coach

