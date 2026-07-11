# Tasarım: `analyze_cv` retry + Pydantic doğrulama

**Tarih:** 2026-07-11
**Sahip:** Kişi 2 (CV İşleme & AI Analiz)
**Kapsam:** Yalnızca `backend/services/cv_service.py` + yeni offline testler. Kişi 1'e bağımlı değil.

## Amaç

Rehber Hafta 3 maddesi "Structured output garanti (JSON mode / function calling + şema
doğrulama + retry)" şu an yarım: JSON mode ve Pydantic şeması var, ama **retry yok** ve
LLM çıktısı Pydantic ile **doğrulanmıyor** (`analyze_cv` ham `json.loads(...)` dict döndürüyor).
Bu tasarım o iki eksiği kapatır ve `analyze_cv`'yi ileride `/cv/upload` entegrasyonu (Hafta 4)
için güvenilir bir birim hâline getirir.

## Mevcut durum

`CVAnalysisService.analyze_cv(cv_text)`:
- Tek Gemini çağrısı (`gemini-2.5-flash`, `response_mime_type=application/json`,
  `response_schema`, `temperature=0.2`).
- `json.loads(response.text)` ile **ham dict** döndürür — Pydantic doğrulaması yok.
- Hata olursa son exception'ı olduğu gibi `raise` eder; retry yok.

Çağıranlar sonucun **dict** olmasına dayanıyor:
- `run_cv_tests.py`: `result.get('experience_years')`, `result.get('role_scores', {}).items()`,
  `json.dump(result, ...)`.
- `test_prompt.py`: benzer dict kullanımı.
- CLAUDE.md tek-satırlık örneği: `print(...analyze_cv(...))`.

## Kararlar

| Karar | Seçim |
|---|---|
| Retry tetikleyici | Hem geçici API hataları hem çıktı/şema hataları |
| Deneme sayısı | Toplam 3 |
| Backoff | API hatası → artan bekleme (1sn → 2sn); çıktı hatası → beklemeden hemen |
| Nihai başarısızlık | Yeni `CVAnalysisError` fırlat (`raise ... from last_error`) |
| Başarı dönüş tipi | **dict** kalır (`validated.model_dump()`) — çağıranları bozmamak için |

## Davranış

`analyze_cv(cv_text)` en fazla 3 deneme yapar. Her denemede sırayla:

1. Gemini `generate_content` çağrısı (system_instruction/config aynen korunur).
2. `json.loads(response.text)`.
3. `CVAnalysisOutput(**data)` ile doğrulama.
4. Başarılıysa `validated.model_dump()` (dict) döndür ve çık.

Hata sınıflandırması:

- **Çıktı hatası** — `json.JSONDecodeError` veya Pydantic `ValidationError`:
  son denemeye kadar **beklemeden** tekrar dene. (Model bir sonraki denemede düzgün
  JSON/şema üretebilir; `temperature=0.2` deterministik değil.)
- **API hatası** — yukarıdakiler dışındaki her exception (timeout, 429 rate limit, 5xx):
  **artan bekleme** (deneme 1 sonrası 1sn, deneme 2 sonrası 2sn) sonra tekrar dene.

3 deneme de tükenirse `CVAnalysisError` fırlatılır; orijinal sebep `from` ile zincirlenir.

## Yapı

Hepsi `backend/services/cv_service.py` içinde (tek dosya, mevcut desen):

- `CVAnalysisError(Exception)` — modül düzeyinde yeni istisna. `cv_parser.CVParseError`
  ile aynı deseni izler: ham kütüphane hatası çağırana sızmaz, tek anlamlı hata tipi.
- Sabitler: `MAX_ATTEMPTS = 3`, `BACKOFF_BASE_SECONDS = 1.0` (deneme *k* sonrası bekleme
  `BACKOFF_BASE_SECONDS * k`, yani 1sn, 2sn).
- `analyze_cv` gövdesi retry döngüsüne dönüşür. Gemini çağrısı/`config`/`system_instruction`
  aynen kalır — yalnızca çevresi sarılır.
- Dönüş tipi **dict** (`model_dump()`).

Bekleme için `time.sleep` kullanılır (import eklenir).

## Hata yönetimi

- Çağırana sızabilecek tek yeni tip: `CVAnalysisError`.
- Doğrulama başarısızlığı sessizce yutulmaz; tüm denemeler tükenirse `CVAnalysisError`'a
  dönüşür.
- Başarılı dönüş her zaman `CVAnalysisOutput` şemasına uygun bir dict'tir (garanti).

## Test (offline — Gemini çağırmadan)

Yeni dosya: `tests/test_cv_service.py`. `cv_parser` testleriyle aynı "offline pytest"
desenine oturur (kota harcamaz, `GEMINI_API_KEY` gerektirmez).

Yöntem: `CVAnalysisService` örneğinin `self.client`'ı **sahte bir client** ile değiştirilir
(gerçek Gemini yerine önceden programlanmış yanıtlar/hatalar döndürür). `__init__` API anahtarı
istediği için testte anahtar mock'lanır ya da örnek doğrudan kurulmadan `client` enjekte edilir.

Kapsanan senaryolar:

1. **Mutlu yol** — client ilk denemede geçerli, şemaya uygun JSON döndürür →
   `analyze_cv` doğru dict döndürür, tek çağrı yapılır.
2. **API hatası sonra başarı** — client ilk çağrıda exception, ikincide geçerli JSON →
   sonunda başarılı dict; beklemenin çağrıldığı doğrulanır (sleep patch'lenir, gerçek
   beklenmez).
3. **Çıktı hatası sonra başarı** — client ilk çağrıda bozuk JSON / şemaya uymayan çıktı
   (örn. `experience_years` string), ikincide düzgün → doğrulama retry'ı tetikler,
   beklemeden tekrar denenir.
4. **Kalıcı başarısızlık** — client her denemede hata → `CVAnalysisError` fırlatılır,
   tam olarak `MAX_ATTEMPTS` çağrı yapılır.

`time.sleep` testlerde patch'lenir ki gerçek beklenmesin (testler hızlı kalsın).

## Kapsam dışı (YAGNI)

- Token/maliyet optimizasyonu (ayrı Hafta 5 maddesi).
- `/cv/upload` entegrasyonu (Hafta 4, Kişi 1 ile koordinasyon gerektirir).
- `cv_parser → cv_service` zincirleme (ayrı iş).
- Yapılandırılabilir retry parametreleri / harici config — sabitler yeterli.

## Hafta 4 bağlantısı

`CVAnalysisError`, ileride `/cv/upload` entegrasyonunda Kişi 1'in yakalayıp temiz bir
HTTP hatasına (örn. 502) çevireceği kancadır — `cv_parser.CVParseError` ile simetrik.
