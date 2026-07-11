# CLAUDE.md

Bu dosya, bu depoda çalışırken Claude Code'a (claude.ai/code) rehberlik eder.

## Bu depo nedir?

"AI Destekli Kariyer Asistanı" — dört kişiye bölünmüş bir bootcamp projesi; her kişi bir modülün ve bir branch'in sahibi. Bu çalışma kopyasında bu modüllerden üçü birleştirilmiş durumda:

- **Kişi 2 / AI çekirdek** (buradaki asıl rol): `backend/services/cv_service.py`, `backend/services/cv_parser.py`, `backend/schemas/` ve kök dizindeki sürücü scriptleri.
- **Kişi 1 / backend iskeleti**: `backend/main.py`, `routers/`, `models/`.
- **Kişi 4 / RAG**: `backend/services/{embedding,ingest_jobs,search_jobs}.py`.
- **Kişi 3 / frontend**: `frontend/` (React + Vite + Tailwind). Backend'den tamamen ayrı bir ağaç; Python tarafına dokunmaz.

Kod yorumları, promptlar, docstring'ler ve ekrana basılan çıktılar **Türkçe** — bu şekilde kalsın. `README.md` haftalık yol haritasını ve dondurulmuş ekip API kontratını içerir.

## Komutlar

İki farklı "test" türü var, karıştırmayın:

- **`pytest`** (kök dizin) — `tests/` içindeki gerçek, **offline** birim testleri. Şu an yalnızca `cv_parser`'ı kapsar; Gemini'yi çağırmaz, kota harcamaz, `GEMINI_API_KEY` gerektirmez. PDF/DOCX test dosyaları diske checked-in edilmez, test içinde `reportlab`/`python-docx` ile üretilir. `pytest.ini`, `pythonpath = backend` ve `testpaths = tests` ayarlar; bu yüzden `pytest` kök dizinden import sorunsuz çalışır. Linter veya build yapılandırması yok, `pyproject.toml` yok.
- **`run_cv_tests.py` / `test_prompt.py`** (kök dizin) — bunlar birim testi değil, **canlı Gemini API'sini** çağıran sürücü scriptleridir; kota harcarlar ve kök dizindeki `.env` içinde `GEMINI_API_KEY` gerektirirler.

Sanal ortam, kök dizindeki `venv/` klasörüdür (README'nin ima ettiği `backend/.venv` değil):

```bash
.\venv\Scripts\Activate.ps1          # PowerShell
pip install -r requirements.txt
```

**Her giriş noktasının zorunlu bir çalışma dizini vardır.** Import'lar bare/relative olduğu için başka dizinlerde kırılırlar:

| Çalıştırılacak dizin | Komut | Amaç |
|---|---|---|
| kök dizin | `pytest` | Offline birim testleri (`cv_parser`) — Gemini çağırmaz |
| kök dizin | `pytest tests/test_cv_parser.py::test_pdf_metni_cikarilir` | Tek bir testi çalıştır |
| `backend/` | `uvicorn main:app --reload` | http://127.0.0.1:8000 üzerinde API (Swagger `/docs`). Canlı: `/chat`; mock: `/cv/upload` |
| `backend/` | `python test_relevance.py [N]` | (canlı Gemini + ChromaDB) ham CV vs. skills-metni arama kalitesi kıyası + kalibrasyon floor probe'u |
| kök dizin | `python run_cv_tests.py` | (canlı Gemini) `sample_cvs/` içindeki her `.txt` dosyasını analiz eder → `test_results/*.json` |
| kök dizin | `python test_prompt.py` | (canlı Gemini) Tek bir gömülü CV ile tek seferlik duman testi |
| `backend/services/` | `python ingest_jobs.py` | `data/jobs_dataset.xlsx` dosyasından ChromaDB indeksini oluşturur |
| `backend/services/` | `python search_jobs.py "sorgu"` | Semantik iş ilanı araması |
| `frontend/` | `npm install` sonra `npm run dev` | Vite dev server (React arayüzü); ilk kez `node_modules` yok, install şart |
| `frontend/` | `npm run build` / `npm run lint` | Prod build / `oxlint` |

Tüm `sample_cvs/` klasörü yerine tek bir CV analiz etmek için (dosya bazlı bir flag yok):

```bash
python -c "import sys; sys.path.append('backend'); from services.cv_service import CVAnalysisService; print(CVAnalysisService().analyze_cv(open('sample_cvs/cv_backend.txt', encoding='utf-8').read()))"
```

## Mimari

### Şema, entegrasyon kontratıdır

`schemas/cv_analysis.py` ve `schemas/api_contract.py`, dört kişinin arasındaki dondurulmuş sınırdır — `CVUploadResponse`, Kişi 2'nin `CVAnalysisOutput`'unu ve Kişi 4'ün `JobMatchItem[]`'ini birleştirir. Buradaki bir alanı değiştirmek diğer kişilerin branch'lerini bozar; dolayısıyla bu iki dosyayı lokal kod değil, paylaşılan API olarak ele alın.

Aynı Pydantic modeli çift görev yapıyor: hem HTTP yanıtını tanımlıyor **hem de** yapılandırılmış JSON çıktısı için Gemini'ye `response_schema` olarak veriliyor. `CVAnalysisService._get_clean_schema()`, `model_json_schema()` çıktısından `additionalProperties` alanını özyinelemeli olarak temizler; çünkü Gemini Developer API bu alanı reddeder. Eklenecek her yeni iç içe model bu kısıtı otomatik devralır.

### 22 rol üç ayrı yerde tanımlı

Bir hedef rol eklemek veya yeniden adlandırmak, üçünün de düzenlenmesini gerektirir; aksi hâlde çıktı sessizce bozulur:

1. `schemas/cv_analysis.py` içindeki `RoleScores` alanları — JSON şeklini tanımlar.
2. `cv_service.analyze_cv()` içindeki `system_instruction` içinde sayılan snake_case isimler — Gemini'ye bunları gerçekten doldurtan şey budur.
3. `CVAnalysisService.target_roles` — görünen adlar; şu anda **`analyze_cv` tarafından kullanılmıyor**, yani bağlantı değil dokümantasyon niteliğinde.

Göze çarpmayan bağımlılık: `RoleScores` içindeki her alanın `default=0` değeri var, dolayısıyla üretilen JSON şemasında **hiçbiri `required` değil**. Şema tek başına Gemini'yi 22 rolün tamamını puanlamaya zorlamaz — bunu yapan tek şey promptun kapanış cümlesidir ("Her bir alan için kesinlikle sayısal bir puan hesaplamalı"). Bir rolü prompt metninden çıkarırsanız hata vermez, sessizce `0` döner.

Skorlama, tutarlılık için `temperature=0.2` kullanır; yine de çıktı **deterministik değildir**: `run_cv_tests.py` her yeniden çalıştırıldığında `test_results/*.json` dosyalarını farklı ifade edilmiş strengths/skills değerleriyle yeniden yazar. Oradaki git gürültüsü beklenen bir durumdur; diff'i bir regresyon olarak okumayın.

### CV ayrıştırma katmanı

`services/cv_parser.py`, ham dosya baytlarını düz metne çeviren tek giriş noktasıdır: `extract_text(data: bytes, filename: str) -> str`. Uzantıyı **dosya adından** seçer (içeriği koklamaz): `.pdf` → `pdfplumber`, `.docx` → `python-docx` (tablo hücreleri dâhil — çoğu CV Word'de tabloyla dizilir ve `doc.paragraphs` bunları atlar), `.txt` → utf-8, olmazsa cp1254 fallback (Türkçe Windows dosyaları). Tüm başarısızlıklar tek bir `CVParseError` tipine dönüşür; ham kütüphane hataları dışarı sızmaz. `MIN_TEXT_LENGTH = 30` altındaki çıktı "boş/taranmış" sayılıp reddedilir — "bu geçerli bir CV mi?" kararı bilinçli olarak parser'a değil, LLM analizine bırakılmıştır.

`cv_service.CVAnalysisService` gibi bu da API'ye **bağlı değildir**: `extract_text`'i çağıran tek yer kendi testleridir, `routers/upload.py` hâlâ mock döner. Çıktısı doğrudan `analyze_cv()`'in beklediği metindir; ikisini birleştirmek Hafta 2'nin bitmemiş işi.

### RAG katmanı

`embedding.py` bilinçli olarak hem indeksleme hem de sorgu embedding'lerinin tek kaynağıdır; böylece ikisi asla birbirinden ayrışamaz (`gemini-embedding-001`, 3072 boyut, hâlihazırda L2-normalize). Task type'ları ayırır: saklanan ilanlar için `__call__` üzerinden `RETRIEVAL_DOCUMENT`, aramalar için `embed_query()` üzerinden `RETRIEVAL_QUERY`. Ayrıca rate limit nedeniyle her embed çağrısında 1.2 sn bekler — ingest işleminin dakikalar sürmesinin sebebi budur.

`search_jobs.py`, ChromaDB koleksiyonunu **modül import edilirken** açar; bu yüzden `ingest_jobs.py` çalıştırılmadan import edilirse `NotFoundError: Collection [tech_job_postings] does not exist` hatası verir. İndeks `backend/data/chromadb/` altında durur ve gitignore'dadır — lokalde yeniden üretilmesi gerekir.

**Skor kalibrasyonu göstermeliktir, sıralama değil.** `gemini-embedding` tabanı yüksek olduğu için alakasız sorgular bile ~0.58 cosine benzerliği alır, alakalılar ~0.62–0.68'de sıkışır. `_calibrate()` bir sigmoid'le (`_CALIB_MIDPOINT=0.60`, `_CALIB_STEEPNESS=28`) bu dar bandı sezgisel bir %0–100'e yayar. Fonksiyon **monotondur**: `match_percent` yalnızca gösterimi değiştirir, ilan sıralamasını asla. Parametreler `test_relevance.py`'nin "floor probe"undan ölçülmüştür; dataset ciddi değişirse floor probe'u tekrar koşup ayarlayın (hedef: alakasız <%50, iyi eşleşme ~%86–90).

`build_search_text(analysis)`, ham CV yerine becerilere odaklı damıtılmış bir arama metni üretir (isim/okul/yıl gürültüsünü atar; `strengths` bilinçli dışlanır). `search_jobs_from_analysis(analysis, n)` bunu `search_jobs` ile birleştiren tek çağrılık kolaylıktır; dönen öğeler `JobMatchItem` kontratına birebir uyar. `include_raw=True` yalnızca tanı içindir (frontend/production'da kullanma).

### Chat / AI Koç katmanı (canlı endpoint)

`/chat`, projedeki **ilk uçtan uca çalışan endpoint**tir (`/cv/upload`'ın aksine mock değil). `services/coach_service.py` + `routers/chat.py` üzerinden çalışır:

- `CareerCoachService`, CV analizi + eşleşen ilanları `_build_context()` ile metinsel bir RAG bağlamına çevirir (beceriler, deneyim, güçlü yönler, eksikler, en yüksek 5 rol skoru, ilanlar). `_SYSTEM_PERSONA` modeli yalnızca bu bağlama dayanmaya zorlar. Model `gemini-2.5-flash`, `temperature=0.6`.
- **Oturum hafızası bellek-içidir** (`_sessions` dict); sunucu yeniden başlayınca sıfırlanır. Kalıcılık gerekirse DB'ye taşınacak.
- `get_coach()` **lazy singleton**tır: `GEMINI_API_KEY` yoksa uygulama yine açılır, yalnızca `/chat` isteği `500` döner. LLM patlarsa router `502` verir.
- İki endpoint: `POST /chat/session` (analiz + eşleşmelerle oturum açıp `session_id` döner — orkestrasyonu Kişi 1 çağıracak) ve `POST /chat` (`session_id` yoksa bağlamsız genel oturum açar).
- **Koç ile ilan-arama henüz bağlı değil**: `search_jobs`'u koç import etmez; bağlamı dışarıdan `create_session` ile alır. `main.py`'nin import zinciri `search_jobs`'a değmediği için uygulama ChromaDB indeksi olmadan da açılır. O bağlamı dolduracak orkestrasyon (Kişi 1) henüz yok.

### Henüz bağlanmamış kısımlar

- `POST /cv/upload`, `services/mock_responses.py` içindeki sabit bir fixture döndürür. `CVAnalysisService` API'ye **bağlı değildir**; yalnızca kök dizindeki scriptler üzerinden çalışır.
- `models/` klasörü, taslak hâlindeki declarative SQLAlchemy modelleridir. Engine yok, session yok, `create_all` yok; `main.py` veya `routers/` içinde hiçbir şey bunları import etmiyor.
- `frontend/` çalışan ama içi boş bir kabuktur: gezinme, tasarım sistemi ve bileşenler hazır, fakat hiçbir ekran gerçek backend'e **bağlı değildir**. `Upload` "Analiz et" ile sadece `/dashboard`'a yönlendirir, `Chat` yalnızca yerel `useState` tutar, `src/lib/api.js` sarmalayıcıları henüz hiçbir yerde çağrılmaz.

### Frontend (Kişi 3)

`frontend/`, React 19 + React Router 7 + Vite 8 + Tailwind CSS 4 SPA'sidir; backend'den bağımsız kendi `package.json`'ı vardır. Dikkat edilecek noktalar:

- **Tasarım sistemi tek kaynaktır.** `src/index.css` içindeki `@theme` bloğu tüm paleti CSS değişkeni olarak tanımlar (`primary-50 … primary-950`, `ink`, `muted`, `danger`/`success`). Ayrı `tailwind.config.js` **yoktur** — Tailwind 4, `@tailwindcss/vite` eklentisiyle temayı buradan okur. **Bileşenlerde ham hex yazmayın**, yalnızca bu token'ları kullanın.
- Rotalar `src/App.jsx`'te: `/` → `Login` (menüsüz), `/upload`+`/dashboard`+`/chat` ise ortak `Layout` (üst menü + `<Outlet/>`) içinde.
- Paylaşılan bileşenler `src/components/ui/` (`Button` primary/secondary/ghost varyantlı, `Card` + `Card.Title`, `Input`).
- Backend adresi `VITE_API_URL` env değişkeninden gelir, varsayılan `http://localhost:8000` (uvicorn ile aynı port).

### Import kuralları

`backend/services/` klasöründe `__init__.py` yok; namespace package'lara dayanıyor. Birbiriyle uyumsuz iki stil bir arada bulunuyor:

- `cv_service.py`, `routers/` ve `mock_responses.py`, paket-mutlak import kullanır (`from schemas.cv_analysis import ...`) ve `backend/` dizininin `sys.path` üzerinde olmasını gerektirir — kök scriptler bunu `sys.path.append(...)` ile yapar, `.vscode/settings.json` ise aynısını `python.analysis.extraPaths` ile yansıtır.
- `ingest_jobs.py` / `search_jobs.py`, bare `from embedding import ...` kullanır. Artık ikisi de import başında `sys.path.insert(0, <kendi dizini>)` yaptığı için hem standalone (`python search_jobs.py`) hem paket (`from services.search_jobs import ...`) olarak import edildiklerinde `embedding` çözülür — eski "yalnızca cwd `backend/services/` iken çalışır" kısıtı kalktı. (Yine de `search_jobs.py` koleksiyonu import anında açar; ChromaDB indeksi hâlâ önden gerekir.)
