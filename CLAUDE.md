# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Bu depo nedir?

"AI Destekli Kariyer Asistanı" — dört kişiye bölünmüş bir bootcamp projesi; her kişi bir modülün ve bir branch'in sahibi. Bu çalışma kopyasında modüllerin çoğu birleştirilmiş ve **Hafta 3 orkestrasyonu bağlanmış** durumda:

- **Kişi 2 / AI çekirdek** (buradaki asıl rol): `backend/services/cv_service.py`, `backend/services/cv_parser.py`, `backend/schemas/` ve kök dizindeki sürücü scriptleri.
- **Kişi 1 / backend iskeleti + orkestrasyon**: `backend/main.py`, `routers/`, `models/`, `crud/`, `database.py`, `auth.py`, `dependencies.py`.
- **Kişi 4 / RAG**: `backend/services/{embedding,ingest_jobs,search_jobs}.py`.
- **Kişi 3 / frontend + evals**: `frontend/` (React + Vite + Tailwind, backend'den tamamen ayrı) ve `evals/` (AI kalite ölçümü) + öğrenme planı promptu (`services/learning_service.py`).

Kod yorumları, promptlar, docstring'ler ve ekrana basılan çıktılar **Türkçe** — bu şekilde kalsın. `README.md` haftalık yol haritasını ve dondurulmuş ekip API kontratını içerir.

## Komutlar

Üç farklı "kontrol" türü var, karıştırmayın:

- **`pytest`** (kök dizin) — `tests/` içindeki gerçek, **offline** birim testleri. `cv_parser` ve `cv_service`'i kapsar; ikisi de Gemini'yi çağırmaz (`cv_service` testi sahte client kullanır), kota harcamaz, `GEMINI_API_KEY` gerektirmez. PDF/DOCX test dosyaları diske checked-in edilmez, test içinde `reportlab`/`python-docx` ile üretilir. `pytest.ini`, `pythonpath = backend` ve `testpaths = tests` ayarlar; bu yüzden `pytest` kök dizinden import sorunsuz çalışır.
- **`evals/`** (kök dizin, `python -m evals.…`) — birim testi **değil**, AI çıktısının "iyi mi" olduğunu ölçen eval'ler. Dosya adları bilerek `test_` ile başlamaz ki pytest onları toplamasın. Bir kısmı canlı Gemini çağırır (kota yakar), bir kısmı offline "guard"dır. Bkz. `evals/README.md`.
- **`run_cv_tests.py` / `test_prompt.py`** (kök dizin) — birim testi değil, **canlı Gemini API'sini** çağıran sürücü scriptleridir; kota harcarlar ve kök dizindeki `.env` içinde `GEMINI_API_KEY` gerektirirler.

Sanal ortam, kök dizindeki `venv/` klasörüdür (README'nin ima ettiği `backend/.venv` değil):

```bash
.\venv\Scripts\Activate.ps1          # PowerShell
pip install -r requirements.txt
```

**Ortam değişkenleri** (kök `.env`): `GEMINI_API_KEY` her zaman gerekir. `/auth/*` ve JWT üreten/çözen her şey ayrıca **`JWT_SECRET_KEY`** ister — set edilmemişse `auth.get_secret_key()` `ValueError` fırlatır (uygulama açılır ama login/register/me patlar). `.env.example` şu an yalnızca `GEMINI_API_KEY` listeler; auth ile çalışacaksanız `JWT_SECRET_KEY` elle eklenmeli.

**Her giriş noktasının zorunlu bir çalışma dizini vardır.** Import'lar bare/relative olduğu için başka dizinlerde kırılırlar:

| Çalıştırılacak dizin | Komut | Amaç |
|---|---|---|
| kök dizin | `pytest` | Offline birim testleri (`cv_parser`, `cv_service`) — Gemini çağırmaz |
| kök dizin | `pytest tests/test_cv_parser.py::test_pdf_metni_cikarilir` | Tek bir testi çalıştır |
| kök dizin | `python -m evals.guards.role_sync` | 22 rol 3 yerde senkron mu? (offline, 0 çağrı) |
| kök dizin | `python -m evals.scoring.accuracy` | Skorlama doğruluğu (canlı Gemini, kota yakar) |
| `backend/` | `uvicorn main:app --reload` | http://127.0.0.1:8000 üzerinde API (Swagger `/docs`). Artık **hepsi canlı**: `/cv/upload`, `/cv/{id}`, `/learning-plan`, `/chat`, `/auth/*` |
| `backend/` | `python test_relevance.py [N]` | (canlı Gemini + ChromaDB) ham CV vs. skills-metni arama kalitesi kıyası + kalibrasyon floor probe'u |
| kök dizin | `python run_cv_tests.py` | (canlı Gemini) `sample_cvs/` içindeki her `.txt` dosyasını analiz eder → `test_results/*.json` |
| kök dizin | `python test_prompt.py` | (canlı Gemini) Tek bir gömülü CV ile tek seferlik duman testi |
| `backend/services/` | `python ingest_jobs.py` | `data/jobs_dataset.xlsx` dosyasından ChromaDB indeksini oluşturur |
| `backend/services/` | `python search_jobs.py "sorgu"` | Semantik iş ilanı araması |
| `frontend/` | `npm install` sonra `npm run dev` | Vite dev server (React arayüzü) |
| `frontend/` | `npm run build` / `npm run lint` | Prod build / `oxlint` |

Tüm `sample_cvs/` klasörü yerine tek bir CV analiz etmek için (dosya bazlı bir flag yok):

```bash
python -c "import sys; sys.path.append('backend'); from services.cv_service import CVAnalysisService; print(CVAnalysisService().analyze_cv(open('sample_cvs/cv_backend.txt', encoding='utf-8').read()))"
```

## Mimari

### API artık uçtan uca bağlı (Hafta 3 orkestrasyonu)

Eski durumun aksine `/cv/upload` **mock değil, canlı** ve tam pipeline'ı çalıştırıyor. Akış:

```
routers/upload.py  → services/upload_service.py.process_cv_upload()
   1. _validate_upload  (uzantı .pdf/.docx, boyut ≤ 5MB, content-type)
   2. cv_parser.extract_text(bytes, filename)          → düz metin
   3. crud.cv_pipeline.create_cv_record(...)           → DB: cvs
   4. CVAnalysisService().analyze_cv(text)             → Gemini (canlı)
   5. search_jobs_from_analysis(analysis, n=5)         → RAG (best-effort; patlarsa boş liste)
   6. crud.cv_pipeline.save_analysis_and_matches(...)  → DB: analyses + job_matches
   7. crud.cv_pipeline.build_upload_response(...)      → tek CVUploadResponse
```

Adım 5 bilinçli **best-effort**: ChromaDB indeksi yoksa veya RAG patlarsa `except Exception → top_matches = []` ile yutulur, upload yine başarılı döner. Yani ChromaDB indeksi olmadan da upload çalışır, sadece `top_matches` boş gelir.

Diğer canlı endpoint'ler:
- `GET /cv/{cv_id}` (`routers/cv.py`) — kayıtlı analizi DB'den `CVUploadResponse` olarak geri okur (`build_cv_detail_response`).
- `POST /learning-plan` (`routers/learning_plan.py`) — hedef role göre öğrenme planı; DB cache'li (aşağıda).
- `POST /auth/{register,login,me}` (`routers/auth.py`) — JWT kimlik doğrulama.
- `POST /chat` + `POST /chat/session` (`routers/chat.py`) — AI koç (aşağıda).

> **Dikkat:** `routers/upload.py` ve `routers/cv.py` **ikisi de** `prefix="/cv"` kullanır. Çakışma yok çünkü biri `POST /cv/upload`, diğeri `GET /cv/{cv_id}`. Yeni bir `/cv/...` rotası eklerken bunu unutmayın.

### Kalıcılık katmanı (SQLite + SQLAlchemy)

`models/` artık taslak değil, **gerçekten kullanılan** declarative modeller: `User`, `CV`, `Analysis`, `JobMatch`, `LearningPlan` (hepsi `models/base.py`'deki tek `Base`'i paylaşır). `database.py` engine'i kurar (`sqlite:///backend/data/app.db`), `init_db()` uygulama açılışında (`main.py` lifespan) `Base.metadata.create_all` çağırır ve `data/uploads/` klasörünü oluşturur. Migration aracı **yok** — şema değişince `app.db`'yi silip yeniden yaratmak gerekir. `app.db`, `data/uploads/` ve `data/chromadb/` gitignore'dadır; lokalde yeniden üretilir.

`crud/cv_pipeline.py` tüm DB erişiminin ve **cevap kurulumunun** tek yeridir — router'lar SQLAlchemy'e doğrudan dokunmaz. Analiz JSON'u DB'ye `*_json` TEXT sütunlarına `json.dumps(..., ensure_ascii=False)` ile serialize edilir, geri okurken `analysis_to_dict` deserialize eder. `build_upload_response`, ham analiz dict'ini `CVUploadResponse`'a (analysis + top_matches + role_rankings) çeviren tek fonksiyondur; hem canlı upload hem DB'den geri-okuma bunu kullanır.

### Şema, entegrasyon kontratıdır

`schemas/cv_analysis.py`, `schemas/api_contract.py` ve `schemas/learning_plan.py`, dört kişinin arasındaki dondurulmuş sınırdır. `CVUploadResponse`, Kişi 2'nin `CVAnalysisOutput`'unu, Kişi 4'ün `JobMatchItem[]`'ini ve Kişi 3'ün `RankedRole[]`'ini (rol sıralaması) birleştirir. Bu dosyalardaki bir alanı değiştirmek diğer kişilerin branch'lerini bozar; lokal kod değil, paylaşılan API olarak ele alın.

Aynı Pydantic modeli çift görev yapıyor: hem HTTP yanıtını tanımlıyor **hem de** yapılandırılmış JSON çıktısı için Gemini'ye `response_schema` olarak veriliyor. `cv_service` ve `learning_service` **ayrı ayrı** `_get_clean_schema()` ile `model_json_schema()` çıktısından `additionalProperties` alanını özyinelemeli temizler; çünkü Gemini Developer API bu alanı reddeder. Yeni bir servis Gemini'ye structured output verecekse aynı temizliği yapmalı.

### 22 rol artık ÜÇ Python nesnesinde tanımlı (bir de prompt metni)

Bir hedef rol eklemek/yeniden adlandırmak dört yerin hepsini gerektirir; aksi hâlde çıktı sessizce bozulur:

1. `schemas/cv_analysis.py` → `RoleScores` alanları — skorların JSON şeklini tanımlar.
2. `cv_service.analyze_cv()` içindeki `system_instruction`'da sayılan snake_case isimler — Gemini'ye 22 rolü gerçekten doldurtan tek şey.
3. `schemas/learning_plan.py` → `TargetRole` enum — öğrenme planının kabul ettiği roller (`rank_roles` bunu iterler).
4. `services/learning_service.py` → `ROLE_DISPLAY` dict — görünen Türkçe adlar; prompt'a girdiği için düzgün Türkçe olmak zorunda.

**Bu senkronu `python -m evals.guards.role_sync` otomatik doğrular** (offline, 0 çağrı): `RoleScores` alanları == `TargetRole` değerleri == `ROLE_DISPLAY` anahtarları. Rol düzenledikten sonra bunu koşun. (Not: `CVAnalysisService.target_roles` hâlâ vardır ama `analyze_cv` tarafından kullanılmaz — dokümantasyon niteliğinde, guard onu kontrol etmez.)

Göze çarpmayan bağımlılık: `RoleScores` alanlarının `default=0` değeri var, dolayısıyla şemada **hiçbiri `required` değil**. 22 rolü doldurtan tek şey promptun kapanış cümlesidir. Bir rolü prompt metninden çıkarırsanız hata vermez, sessizce `0` döner.

Skorlama `temperature=0.2` kullanır ama çıktı **deterministik değildir**: `run_cv_tests.py` ve eval'ler her koşuda farklı ifade edilmiş strengths/skills üretir. Oradaki git gürültüsü beklenendir; diff'i regresyon olarak okumayın.

Kullanılan model her yerde **`gemini-3.5-flash`** (cv_service, coach_service, learning_service). Embedding ise `gemini-embedding-001`.

### CV ayrıştırma katmanı

`services/cv_parser.py`, ham dosya baytlarını düz metne çeviren tek giriş noktasıdır: `extract_text(data: bytes, filename: str) -> str`. Uzantıyı **dosya adından** seçer: `.pdf` → `pdfplumber`, `.docx` → `python-docx` (tablo hücreleri dâhil), `.txt` → utf-8, olmazsa cp1254 fallback. Tüm başarısızlıklar tek bir `CVParseError` tipine dönüşür. `MIN_TEXT_LENGTH = 30` altındaki çıktı "boş/taranmış" sayılıp reddedilir — "bu geçerli bir CV mi?" kararı bilinçli olarak LLM analizine bırakılmıştır. Artık `upload_service` tarafından canlı çağrılıyor; `.pdf`/`.docx` dışı upload'lar `_validate_upload`'ta zaten elenir.

### RAG katmanı

`embedding.py`, hem indeksleme hem sorgu embedding'lerinin tek kaynağıdır (`gemini-embedding-001`, 3072 boyut, L2-normalize). Task type ayrımı: saklanan ilanlar `RETRIEVAL_DOCUMENT`, aramalar `RETRIEVAL_QUERY`. Rate limit için her embed çağrısında 1.2 sn bekler — ingest'in dakikalar sürme sebebi budur.

`search_jobs.py`, ChromaDB koleksiyonunu **modül import edilirken** açar; bu yüzden `ingest_jobs.py` çalıştırılmadan import edilirse `NotFoundError` verir. Bu yüzden `upload_service` onu **fonksiyon içinde geç import eder** (`from services.search_jobs import ...`) ve `except`'e sarar — böylece indeks yokken uygulama yine ayağa kalkar ve upload çalışır.

**Skor kalibrasyonu göstermeliktir, sıralama değil.** `gemini-embedding` tabanı yüksek olduğu için alakasız sorgular ~0.58, alakalılar ~0.62–0.68 cosine alır. `_calibrate()` bir sigmoid'le (`_CALIB_MIDPOINT=0.60`, `_CALIB_STEEPNESS=28`) bu dar bandı %0–100'e yayar; **monotondur**, yalnızca gösterimi değiştirir, ilan sıralamasını asla. Parametreler `test_relevance.py`'nin floor probe'undan ölçülür; dataset değişirse probe'u tekrar koşun (hedef: alakasız <%50, iyi eşleşme ~%86–90).

`build_search_text(analysis)`, ham CV yerine becerilere odaklı damıtılmış metin üretir (`strengths` bilinçli dışlanır). `search_jobs_from_analysis(analysis, n)` bunu `search_jobs` ile birleştirir; dönen öğeler `JobMatchItem` kontratına birebir uyar.

### Öğrenme planı katmanı (canlı endpoint, cache'li)

`POST /learning-plan` iki servise bölünür:

- `services/learning_service.py` → `LearningPathService` DB/HTTP/cv_id bilmez; saf Gemini işidir. `build_plan(target_role, gaps, skills)` tek rol için tek çağrı yapar, **429 için üstel geri çekilmeli yeniden deneme** içerir ve günlük kotayı (`PerDay`) tespit edip boşuna beklemeden hata verir. Prompt'u 12 katı kuralla çok detaylı (alan uyumu, kaynak tipi, ücret etiketi, uydurma yasağı). Ayrıca `rank_roles(role_scores)` ve `ROLE_DISPLAY` buradadır.
- `services/learning_plan_service.py` → `create_learning_plan` orkestrasyondur: CV+analizi DB'den bulur, **aynı (analysis_id, target_role) için plan varsa Gemini'yi hiç çağırmaz** (`cached=True` döner), yoksa üretip DB'ye yazar. `gaps_for_target_role` ile role etiketli gap'leri (`[devops_engineer] ...`) filtreler.

### Chat / AI Koç katmanı

`services/coach_service.py` + `routers/chat.py`. `CareerCoachService`, CV analizi + eşleşen ilanları `_build_context()` ile metinsel RAG bağlamına çevirir; `_SYSTEM_PERSONA` modeli yalnızca bu bağlama dayanmaya zorlar (`temperature=0.6`).

- **Oturum hafızası bellek-içidir** (`_sessions` dict); sunucu yeniden başlayınca sıfırlanır.
- `get_coach()` **lazy singleton**tır: `GEMINI_API_KEY` yoksa uygulama açılır, yalnızca `/chat` isteği hata verir.
- İki endpoint: `POST /chat/session` (analiz + eşleşmelerle oturum açıp `session_id` döner) ve `POST /chat` (bağlamsız genel oturum).
- Koç `search_jobs`'u import etmez; bağlamı dışarıdan `create_session` ile alır — bu yüzden import zinciri ChromaDB'ye değmez.

### Kimlik doğrulama

`auth.py` JWT üretir/çözer (`python-jose`, HS256, 24 saat) ve parola hash'ler (`passlib[bcrypt]`). `dependencies.py` iki bağımlılık sunar: `get_current_user` (token zorunlu, yoksa 401) ve `get_current_user_optional` (token yoksa `None` — upload anonim de çalışsın diye). `CV.user_id` nullable olduğundan giriş yapmadan da CV yüklenebilir. `JWT_SECRET_KEY` gerekir (yukarı bkz.).

### Frontend (Kişi 3)

`frontend/`, React 19 + React Router 7 + Vite 8 + Tailwind CSS 4 SPA'sidir; backend'den bağımsız kendi `package.json`'ı vardır.

- **Tasarım sistemi tek kaynaktır.** `src/index.css` içindeki `@theme` bloğu tüm paleti CSS değişkeni olarak tanımlar. Ayrı `tailwind.config.js` **yoktur** — Tailwind 4, `@tailwindcss/vite` eklentisiyle temayı buradan okur. **Bileşenlerde ham hex yazmayın**, yalnızca token'ları kullanın.
- Rotalar `src/App.jsx`'te: `/` → `Login` (menüsüz); `/upload`+`/dashboard`+`/chat` ortak `Layout` içinde.
- Backend adresi `VITE_API_URL`, varsayılan `http://localhost:8000`. CORS `main.py`'de `localhost:5173` için açık.
- Frontend hâlâ büyük ölçüde backend'e **bağlı değildir** (ekranlar `src/lib/api.js` sarmalayıcılarını henüz çağırmaz); backend tarafı artık hazır olsa da bağlama işi Kişi 3'te.

### Import kuralları

`backend/services/`, `crud/`, `routers/`, `models/`, `schemas/` paket-mutlak import kullanır (`from schemas.cv_analysis import ...`) ve `backend/` dizininin `sys.path` üzerinde olmasını gerektirir — bu yüzden `uvicorn` `backend/` içinden çalıştırılır, kök scriptler `sys.path.append('backend')` yapar, eval'ler `python -m` ile koşar (`evals/_paths.py` yolu ayarlar).

İstisna: `ingest_jobs.py` / `search_jobs.py` bare `from embedding import ...` kullanır ama import başında `sys.path.insert(0, <kendi dizini>)` yaptığı için hem standalone hem paket olarak çözülür. (Yine de `search_jobs.py` koleksiyonu import anında açar; ChromaDB indeksi hâlâ önden gerekir — bu yüzden `upload_service` onu geç import eder.)

`backend/services/`'de `__init__.py` yok (namespace package); `crud/`, `routers/`, `models/`, `schemas/`, `core/` ise `__init__.py` içerir.
