# Backend — Hafta 3 (Kişi 1)

Bu branch (`feature/kisi1-hafta3-backend`), Hafta 2 üzerine **tam orkestrasyon, öğrenme planı endpoint'i, rol sıralaması ve logging** ekler.

**Hafta 3 kapsamı:**
- Upload → parse → analiz → RAG → DB → tek JSON (orkestrasyon)
- `GET /cv/{cv_id}` ile kayıtlı sonucu getirme
- `POST /learning-plan` ile hedef role göre plan üretme (Kişi 3 servisi)
- Yapılandırılmış logging ve merkezi hata yönetimi

---

## Branch'i çekme

```bash
git clone https://github.com/afragul/YZTA-Bootcamp.git
cd YZTA-Bootcamp
git checkout feature/kisi1-hafta3-backend
```

---

## Kurulum

### 1. Sanal ortam

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 2. Bağımlılıklar

```bash
pip install -r ../requirements.txt
```

### 3. Ortam değişkenleri

```bash
cp .env.example .env
```

`.env` dosyasına ekleyin:

```
GEMINI_API_KEY=your_key_here
JWT_SECRET_KEY=uzun_rastgele_bir_string
```

### 4. ChromaDB (iş ilanı eşleştirme — ilk seferde)

```bash
python services/ingest_jobs.py
```

> Ingest yapılmamışsa upload yine çalışır; `top_matches` boş döner.

---

## API'yi çalıştırma

```bash
cd backend
uvicorn main:app --reload
```

Sunucu: **http://127.0.0.1:8000**

| Adres | Açıklama |
|---|---|
| http://127.0.0.1:8000/docs | Swagger UI — endpoint test |
| http://127.0.0.1:8000/redoc | ReDoc dokümantasyon |
| http://127.0.0.1:8000/openapi.json | OpenAPI şeması |

---

## Önerilen kullanım akışı (Frontend / ekip)

```
1. POST /cv/upload          → cv_id + analysis + top_matches + role_rankings
2. GET  /cv/{cv_id}         → (isteğe bağlı) sonucu tekrar getir
3. POST /learning-plan      → kullanıcının seçtiği hedef role göre plan
4. POST /chat/session       → analysis + top_matches ile koç oturumu aç
5. POST /chat               → koçla konuş
```

---

## Endpoint'ler

### `GET /health`

```bash
curl http://127.0.0.1:8000/health
```

```json
{ "status": "ok", "service": "ai-kariyer-asistani-backend" }
```

---

### `POST /auth/register`

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"sifre12345"}'
```

---

### `POST /auth/login`

Swagger'da **Authorize** veya:

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -d "username=user@example.com&password=sifre12345"
```

```json
{ "access_token": "eyJ...", "token_type": "bearer" }
```

---

### `POST /cv/upload`

PDF veya DOCX yükler (max **5 MB**). Bearer token **opsiyonel** — varsa CV kullanıcıya bağlanır.

**Orkestrasyon akışı:**
```
dosya doğrulama → cv_parser (Kişi 2)
               → cv_service  (Kişi 2)
               → search_jobs (Kişi 4)
               → SQLite kayıt
               → tek JSON cevap
```

```bash
curl -X POST http://127.0.0.1:8000/cv/upload \
  -F "file=@ornek_cv.pdf"
```

**Örnek cevap (özet):**
```json
{
  "cv_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "ornek_cv.pdf",
  "status": "completed",
  "message": "CV basariyla yuklendi, analiz edildi ve is ilanlari eslestirildi.",
  "analysis": {
    "skills": ["Python", "FastAPI"],
    "experience_years": 1.5,
    "education": [],
    "strengths": ["..."],
    "gaps": ["[backend_developer] Docker deneyimi eksik"],
    "role_scores": { "backend_developer": 85, "frontend_developer": 70 },
    "top_role_reasons": [
      { "role": "backend_developer", "score": 85, "reason": "..." }
    ]
  },
  "top_matches": [
    {
      "title": "Backend Developer",
      "job_domain": "Backend",
      "work_type": "Remote",
      "job_location": "Istanbul",
      "match_percent": 88.5,
      "description": "..."
    }
  ],
  "role_rankings": [
    {
      "rank": 1,
      "role": "backend_developer",
      "display": "Backend Geliştirici",
      "score": 85,
      "auto": true
    }
  ]
}
```

`role_rankings`: 22 rol skora göre sıralı. Frontend rol seçiciyi bununla besler.
- `auto: true` → sadece rank=1 (en yüksek skorlu rol)
- Kullanıcı hedef rolü **kendisi seçer** → `POST /learning-plan`'e gönderilir

---

### `GET /cv/{cv_id}`

Upload cevabıyla **aynı JSON yapısını** DB'den getirir.

```bash
curl http://127.0.0.1:8000/cv/550e8400-e29b-41d4-a716-446655440000
```

---

### `POST /learning-plan`

Kullanıcının seçtiği hedef role göre öğrenme planı üretir (Kişi 3 — `LearningPathService`).

```bash
curl -X POST http://127.0.0.1:8000/learning-plan \
  -H "Content-Type: application/json" \
  -d '{
    "cv_id": "550e8400-e29b-41d4-a716-446655440000",
    "target_role": "machine_learning_engineer"
  }'
```

**Örnek cevap:**
```json
{
  "cv_id": "550e8400-e29b-41d4-a716-446655440000",
  "target_role": "machine_learning_engineer",
  "cached": false,
  "plan": {
    "target_role": "machine_learning_engineer",
    "summary": "...",
    "total_weeks": 6,
    "weeks": [
      {
        "week": 1,
        "focus": "Python veri bilimi temelleri",
        "steps": [
          {
            "order": 1,
            "topic": "NumPy ve Pandas",
            "reason": "...",
            "resource_type": "kurs",
            "resource_suggestion": "...",
            "estimated_hours": 8
          }
        ]
      }
    ]
  }
}
```

> Aynı `cv_id` + `target_role` için ikinci istek `cached: true` döner (DB cache).

**Geçerli `target_role` değerleri** (`schemas/learning_plan.py` → `TargetRole` enum):
`backend_developer`, `frontend_developer`, `machine_learning_engineer`, `data_scientist`, `devops_engineer`, ... (toplam 22 rol)

---

### Chat (Kişi 4)

```bash
# Oturum aç
curl -X POST http://127.0.0.1:8000/chat/session \
  -H "Content-Type: application/json" \
  -d '{"analysis": {...}, "top_matches": [...]}'

# Mesaj gönder
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hangi rol bana daha uygun?", "session_id": "..."}'
```

---

## Ekip entegrasyon tablosu

| Kişi | Modül | Endpoint / alan |
|---|---|---|
| **Kişi 1** | Orkestrasyon | `POST /cv/upload`, `GET /cv/{cv_id}`, `POST /learning-plan` |
| **Kişi 2** | CV analiz | `analysis` → `CVAnalysisOutput` |
| **Kişi 3** | Rol skorlama + plan | `role_rankings`, `POST /learning-plan` |
| **Kişi 4** | RAG + chat | `top_matches[]`, `/chat/session`, `/chat` |
| **Frontend** | UI | Upload → dashboard (skorlar) → rol seç → plan → chat |

---

## Proje yapısı (Hafta 3)

```
backend/
├── main.py                       # FastAPI + logging + hata handler'ları
├── core/
│   └── logging_config.py
├── database.py                   # SQLite bağlantısı
├── auth.py                       # JWT + bcrypt
├── routers/
│   ├── health.py
│   ├── auth.py                   # register / login / me
│   ├── upload.py                 # POST /cv/upload
│   ├── cv.py                     # GET /cv/{cv_id}
│   ├── learning_plan.py          # POST /learning-plan
│   └── chat.py                   # chat/session + chat
├── schemas/
│   ├── api_contract.py           # Tüm endpoint kontratları
│   ├── cv_analysis.py            # Kişi 2 analiz şeması
│   └── learning_plan.py          # Kişi 3 plan şeması
├── crud/
│   ├── users.py
│   └── cv_pipeline.py            # CV / analiz / plan CRUD
├── models/                       # SQLAlchemy (User, CV, Analysis, JobMatch, LearningPlan)
└── services/
    ├── cv_parser.py              # Kişi 2 — PDF/DOCX parse
    ├── cv_service.py             # Kişi 2 — Gemini analiz
    ├── learning_service.py       # Kişi 3 — öğrenme planı agent
    ├── learning_plan_service.py  # Plan orkestrasyon katmanı
    ├── upload_service.py         # Upload orkestrasyon katmanı
    ├── search_jobs.py            # Kişi 4 — RAG arama
    └── coach_service.py          # Kişi 4 — AI koç
```

---

## Haftalık ilerleme (Kişi 1)

| Hafta | Durum | Görevler |
|---|---|---|
| **Hafta 1** | ✅ | FastAPI iskelet, API kontratı, mock endpoint'ler |
| **Hafta 2** | ✅ | Gerçek upload, SQLite CRUD, JWT auth |
| **Hafta 3** | ✅ | Tam orkestrasyon, learning-plan, logging |
| **Hafta 4** | 🔜 | Loading/polling, chat otomatik bağlama |
| **Hafta 5** | 🔜 | Docker, deploy, production |

---

## Sorun giderme

**`ModuleNotFoundError: No module named 'routers'`**
```bash
cd backend && uvicorn main:app --reload
```

**`GEMINI_API_KEY bulunamadi`**
`.env` dosyasını kontrol edin; `backend/` klasöründe olmalı.

**`top_matches` boş geliyor**
```bash
python services/ingest_jobs.py
```

**422 — geçersiz CV**
Yüklenen dosya CV değil veya çok kısa; geçerli bir PDF/DOCX CV deneyin.

**502 — analiz hatası**
Gemini API anahtarı veya kota sorunu; log çıktısına bakın.

**Port meşgul**
```bash
uvicorn main:app --reload --port 8001
```
