# Backend — Hafta 1 (Kişi 1)

Bu branch (`feature/kisi1-hafta1-backend`), **AI Kariyer Asistanı** projesinin backend iskeletini içerir.  
Amaç: Ekip arkadaşlarının (Kişi 2–4 ve Frontend) entegrasyona başlayabilmesi için **dondurulmuş API kontratı** ve çalışan temel endpoint'ler sunmaktır.

---

## Branch'i çekme

```bash
git clone https://github.com/afragul/YZTA-Bootcamp.git
cd YZTA-Bootcamp
git checkout feature/kisi1-hafta1-backend
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

### 3. Ortam değişkenleri (opsiyonel — Hafta 1 için zorunlu değil)

ChromaDB / Gemini servisleri (`services/ingest_jobs.py`, `services/search_jobs.py`) için:

```bash
# backend/.env
GEMINI_API_KEY=your_key_here
```

> Hafta 1 API endpoint'leri mock veri döndürür; `.env` olmadan da `/health` ve `/cv/upload` çalışır.

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

## Aktif endpoint'ler (Hafta 1)

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

### `POST /cv/upload` *(mock)*

CV dosyası yükler. **Hafta 1'de gerçek analiz yapılmaz** — ekip entegrasyonu için sabit mock JSON döner.

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
