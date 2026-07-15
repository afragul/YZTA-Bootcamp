# Tasarım: Edge case'ler — geçersiz CV'de güvenli cevap

**Tarih:** 2026-07-11
**Sahip:** Kişi 2 (CV İşleme & AI Analiz)
**Kapsam:** Yalnızca `backend/services/cv_service.py` + offline testler. Şemaya dokunmaz; Kişi 1/3/4'e bağlı değildir.

## Amaç

Rehber Kişi 2 – Hafta 4 maddesi "Edge case'ler: çok kısa CV, alakasız belge, boş alan → güvenli cevap".
Şu an `analyze_cv`, geçerli uzunlukta ama CV olmayan bir girdiyi (tarif, haber, rastgele metin)
doğrudan Gemini'ye gönderiyor; Gemini şemaya uygun ama **uydurma** bir analiz üretiyor
(hayali beceriler, rastgele rol skorları). Bu tasarım, geçersiz girdiyi tespit edip
uydurma analiz yerine net bir hata sinyali verir.

Not: `cv_parser.extract_text` dosya seviyesindeki edge case'leri (boş dosya, <30 karakter,
desteklenmeyen tip, bozuk dosya, taranmış PDF → `CVParseError`) zaten yönetiyor. Bu tasarım
**analiz katmanındaki** boşluğu kapatır: `analyze_cv` doğrudan da çağrılabildiği için kendi
girdi savunmasına sahip olmalı, ve "alakasız belge" hiçbir katmanda yakalanmıyor.

## Mevcut durum

`analyze_cv(cv_text)` şu an: Python girdi kontrolü yok; doğrudan retry döngüsüne girip
`_attempt_analysis`'i çağırıyor, sonucu (dict) döndürüyor. Geçersiz/alakasız girdi için
özel davranış yok.

## Kararlar

| Karar | Seçim |
|---|---|
| Güvenli cevap şekli | Yeni `InvalidCVError` istisnası (Kişi 1 → HTTP 422) |
| Tespit yöntemi | Hibrit: Python uzunluk kontrolü + Gemini "boş döndür" sinyali |
| Katman 2 kontrol yeri | Retry döngüsü DIŞINDA (başarılı sonuçtan sonra) |
| Etkin-boş kriteri | `skills == []` VE tüm `role_scores` değerleri `0` (muhafazakâr AND) |
| Eşik | `MIN_CV_TEXT_LENGTH = 40` |
| Bağımsızlık | Şema değişmez; sadece prompt + `analyze_cv` mantığı |

## Davranış

Yeni `InvalidCVError(Exception)` — modül düzeyinde, `cv_service.py`'de.

`analyze_cv(cv_text)` iki katmanlı savunma kazanır:

**Katman 1 — Python uzunluk kontrolü (Gemini çağrısı YOK):**
`analyze_cv`'nin en başında, retry döngüsünden önce:
- `cv_text` `None`/boş veya `len(cv_text.strip()) < MIN_CV_TEXT_LENGTH` ise → hemen
  `InvalidCVError` fırlat. Gemini çağrılmaz, kota harcanmaz.

**Katman 2 — Gemini sinyali (alakasız belge):**
- Prompt'a yeni kural: metin bir CV/özgeçmiş değilse (tarif, haber, rastgele metin) model
  TÜM alanları boş/0 döndürmeli (`skills=[]`, `experience_years=0`, `education=[]`,
  `strengths=[]`, `gaps=[]`, tüm `role_scores=0`, `top_role_reasons=[]`). Bu kural,
  CV değilse skorlama/top_role_reasons kurallarını GEÇERSİZ kılar.
- Retry döngüsü başarılı bir sonuç (doğrulanmış dict) döndürdükten SONRA, `analyze_cv`
  sonucun etkin boş olup olmadığını kontrol eder: `not result["skills"]` VE
  `result["role_scores"]`'un tüm değerleri `0` ise → `InvalidCVError` fırlat.

**Retry ile etkileşim:** Her iki kontrol de retry döngüsünün dışında yer alır (Katman 1
döngüden önce, Katman 2 başarılı sonuçtan sonra). Böylece `InvalidCVError`, retry
döngüsünün `except Exception` dalına düşüp 3 kez boşuna denenmez. Mevcut retry/doğrulama
davranışı (`CVAnalysisError`, backoff) değişmez.

## Yapı

Tek dosya: `backend/services/cv_service.py`.
- `InvalidCVError(Exception)` — yeni istisna.
- `MIN_CV_TEXT_LENGTH = 40` — yeni sabit.
- `_attempt_analysis` içindeki `system_instruction`'a "CV değilse boş döndür" kuralı eklenir.
- `analyze_cv` gövdesi: başına Katman 1 kontrolü, retry döngüsünün başarılı-sonuç yolundan
  önce Katman 2 kontrolü. `_attempt_analysis`, `CVAnalysisError`, retry mantığı korunur.

Şema (`CVAnalysisOutput`), imzalar, dönüş tipi (`dict`) değişmez.

## Bağımsızlık / ekip kontratı

`CVAnalysisOutput` (dondurulmuş ekip kontratı) değişmez; `gaps`/`skills`/`role_scores`
tipleri sabit. Kişi 1/3/4 etkilenmez. `InvalidCVError`, `CVParseError`/`CVAnalysisError`
ile simetrik yeni bir sinyaldir; Kişi 1 orkestrasyonda yakalayıp uygun HTTP koduna
(muhtemelen 422) çevirir.

## Doğrulama

Bu görevin tespit mantığı **deterministik Python** olduğu için offline TDD uygundur
(Madde 1'in prompt-kalite değişikliğinin aksine).

**Offline testler (sahte client, `tests/test_cv_service.py`'ye eklenir):**
1. Çok kısa/boş girdi (`""`, birkaç karakter) → `InvalidCVError`; sahte client'ın
   `generate_content`'i **hiç çağrılmaz** (`calls == 0` ile doğrulanır — Katman 1 API'siz).
2. Sahte client etkin-boş çıktı döndürür (`skills=[]`, tüm `role_scores=0`) →
   `analyze_cv` `InvalidCVError` fırlatır (Katman 2).
3. Regresyon: normal dolu çıktı (`_VALID_OUTPUT`) → hâlâ dict döner, hata yok.
4. Regresyon: mevcut 20 test yeşil kalır.

**Opsiyonel canlı doğrulama:** Bir tarif/haber metnini `analyze_cv`'ye ver → `InvalidCVError`
beklenir (modelin gerçekten boş döndürdüğünü teyit eden göz kontrolü; kota harcar,
deterministik değil).

## Kapsam dışı (YAGNI)

- Şemaya `is_cv`/confidence alanı eklemek (bilinçli olarak bağımsız kalmak için hariç).
- Ayrı Gemini "bu bir CV mi?" ön-kontrol çağrısı (kota/gecikme nedeniyle hariç).
- `cv_parser`'ın dosya-seviyesi edge case'lerini değiştirmek (zaten çözülmüş).
- Anahtar-kelime tabanlı içerik sınıflandırması.
