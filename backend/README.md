# Backend — Hafta 2 (Kişi 1)

Bu branch (`feature/kisi1-hafta2-backend`), Hafta 1 iskeletinin uzerine **gercek upload, SQLite CRUD ve JWT auth** ekler.
Upload akisi: parse (Kisi 2) → analiz (Kisi 2) → RAG eslestirme (Kisi 4) → DB kayit.

---

## Branch'i çekme

```bash
git clone https://github.com/afragul/YZTA-Bootcamp.git
cd YZTA-Bootcamp
git checkout feature/kisi1-hafta2-backend
```

---

## Kurulum

### 1. Sanal ortam (önerilir)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 2. Bağımlılıkları yükle

```bash
pip install -r requirements.txt
```

### 3. Ortam değişkenleri

```bash
cp .env.example .env
# .env icine ekleyin:
# GEMINI_API_KEY=...
# JWT_SECRET_KEY=...   (uzun rastgele bir string)
```

> ChromaDB is ilani eslestirmesi icin once `python services/ingest_jobs.py` calistirin.

---

## API'yi çalıştırma

```bash
cd backend
uvicorn main:app --reload
```

Sunucu varsayılan olarak **http://127.0.0.1:8000** adresinde ayağa kalkar.

---

## API dokümantasyonuna erişim

| Adres | Açıklama |
|---|---|
| http://127.0.0.1:8000/docs | **Swagger UI** — endpoint'leri tarayıcıdan test edin |
| http://127.0.0.1:8000/redoc | ReDoc — okunabilir API dokümantasyonu |
| http://127.0.0.1:8000/openapi.json | OpenAPI şeması (JSON) |

Swagger UI'da **Try it out** ile doğrudan istek atabilirsiniz.

---

## Aktif endpoint'ler (Hafta 2)

### `POST /auth/register`

```json
{ "email": "user@example.com", "password": "sifre123" }
```

### `POST /auth/login`

OAuth2 form: `username` = e-posta, `password` = sifre → `{ "access_token": "...", "token_type": "bearer" }`

### `GET /auth/me`

Bearer token ile giris yapan kullaniciyi dondurur.

### `POST /cv/upload`

PDF veya DOCX yukler (max 5 MB). Bearer token opsiyonel — varsa CV kullaniciya baglanir.

Akis: dosya dogrulama → metin cikarma → Gemini analiz → ChromaDB is eslestirme → SQLite kayit.

---

### `GET /health`

Servisin ayakta olup olmadığını kontrol eder.

**Örnek istek:**
```bash
curl http://127.0.0.1:8000/health
```

**Örnek cevap:**
```json
{
  "status": "ok",
  "service": "ai-kariyer-asistani-backend"
}
```

---

### `POST /cv/upload`

**Hafta 2:** Gercek dosya isleme (mock degil).

**Örnek istek:**
```bash
curl -X POST http://127.0.0.1:8000/cv/upload \
  -F "file=@ornek_cv.pdf"
```

**Örnek cevap yapısı:**
```json
{
  "cv_id": "uuid-string",
  "filename": "ornek_cv.pdf",
  "status": "completed",
  "message": "Mock yanit - Hafta 1 entegrasyon kontrati",
  "analysis": {
    "skills": ["Python", "FastAPI", "..."],
    "experience_years": 1.5,
    "education": [{ "degree": "...", "school": "...", "department": "...", "graduation_year": 2025 }],
    "strengths": ["..."],
    "gaps": ["..."],
    "role_scores": {
      "backend_developer": 85,
      "frontend_developer": 70,
      "machine_learning_engineer": 40,
      "data_scientist": 45,
      "devops_engineer": 50
    }
  },
  "top_matches": [
    {
      "title": "Backend Developer (Python/FastAPI)",
      "job_domain": "Backend",
      "work_type": "Remote",
      "job_location": "Istanbul",
      "match_percent": 88.5,
      "description": "..."
    }
  ]
}
```

---

## API kontratı (ekip için referans)

Tüm JSON şemaları `schemas/` klasöründe tanımlıdır:

| Dosya | İçerik |
|---|---|
| `schemas/cv_analysis.py` | Kişi 2 — CV analiz çıktısı (`CVAnalysisOutput`, `RoleScores`) |
| `schemas/api_contract.py` | Tüm endpoint request/response modelleri |

### Ekip entegrasyon notları

| Kişi | Modül | Kontrat alanı |
|---|---|---|
| **Kişi 2** | CV Analiz | `analysis` objesi → `CVAnalysisOutput` |
| **Kişi 3** | Rol Skorlama | `analysis.role_scores` |
| **Kişi 4** | RAG / İş Eşleştirme | `top_matches[]` → `JobMatchItem` |
| **Frontend** | Upload UI | `POST /cv/upload` multipart form (`file` alanı) |

> Hafta 3'te orkestrasyon endpoint'i de aynı JSON yapısını tek seferde döndürecek.

---

## Proje klasör yapısı

```
backend/
├── main.py                  # FastAPI uygulama girişi
├── routers/
│   ├── health.py            # GET /health
│   └── upload.py            # POST /cv/upload (mock)
├── schemas/
│   ├── api_contract.py      # Endpoint kontratları
│   └── cv_analysis.py         # CV analiz şeması
├── models/                  # SQLAlchemy taslak modeller (Hafta 2'de aktif)
│   ├── user.py
│   ├── cv.py
│   ├── analysis.py
│   ├── job_match.py
│   └── learning_plan.py
├── services/
│   ├── mock_responses.py    # Mock upload cevabı
│   ├── embedding.py         # ChromaDB embedding (Kişi 4)
│   ├── ingest_jobs.py       # İş ilanı yükleme (Kişi 4)
│   └── search_jobs.py       # Semantik arama (Kişi 4)
└── data/
    └── jobs_dataset.xlsx
```

---

## Gelecek haftalar (plan)

| Hafta | Kişi 1 görevleri |
|---|---|
| **Hafta 2** | Gerçek dosya upload (PDF/DOCX), SQLite + SQLAlchemy CRUD, Auth (JWT) |
| **Hafta 3** | Orkestrasyon endpoint (upload → analiz → RAG → DB → JSON) |
| **Hafta 4** | Chat endpoint, loading/polling, hata yönetimi |
| **Hafta 5** | Docker, deploy, production ayarları |

---

## Sorun giderme

**`ModuleNotFoundError: No module named 'routers'`**  
Komutu `backend/` klasörü içinden çalıştırın:
```bash
cd backend && uvicorn main:app --reload
```

**Port meşgul**  
Farklı port kullanın:
```bash
uvicorn main:app --reload --port 8001
```

**Bağımlılık hatası**  
Sanal ortamın aktif olduğundan emin olun:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```
