# Geçersiz CV'de Güvenli Cevap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `analyze_cv`'yi geçersiz girdiye (çok kısa/boş veya alakasız belge) karşı iki katmanlı savunmayla `InvalidCVError` fırlatacak hale getirmek; uydurma analiz üretmesini önlemek.

**Architecture:** `cv_service.py`'de yeni `InvalidCVError` + `MIN_CV_TEXT_LENGTH`. Katman 1: `analyze_cv` başında Python uzunluk kontrolü (API'siz). Katman 2: prompt'a "CV değilse boş döndür" kuralı + retry başarısından sonra etkin-boş kontrolü. Şema değişmez.

**Tech Stack:** Python, `google-genai`, mevcut retry/doğrulama altyapısı, `pytest` (offline, sahte client).

## Global Constraints

- **Şemaya DOKUNMA** — `CVAnalysisOutput` dondurulmuş ekip kontratı. Sadece prompt + `analyze_cv` mantığı + testler.
- **`MIN_CV_TEXT_LENGTH = 40`**; etkin-boş kriteri: `skills == []` VE tüm `role_scores` değerleri `0` (muhafazakâr AND).
- **Katman 2 kontrolü retry döngüsünün DIŞINDA** (başarılı sonuçtan sonra) — `InvalidCVError` retry tetiklememeli.
- Mevcut retry/doğrulama davranışı (`CVAnalysisError`, backoff, `_attempt_analysis`) korunur.
- Yorum/prompt/mesaj Türkçe; yeni bağımlılık yok. Python: `./venv/Scripts/python.exe`.
- Mevcut 20 test + 3 yeni = **23 test** yeşil olmalı.

---

## File Structure

- **Modify:** `backend/services/cv_service.py` — `InvalidCVError`, `MIN_CV_TEXT_LENGTH`, prompt rule 0, `_is_effectively_empty`, `analyze_cv` (Katman 1 + Katman 2).
- **Modify:** `tests/test_cv_service.py` — import güncelle, `_CV_TEXT`/`_EMPTY_OUTPUT` sabitleri, mevcut testlerin kısa girdilerini `_CV_TEXT` ile değiştir, 3 yeni test ekle.

---

## Task 1: `InvalidCVError` + iki katmanlı geçersiz-girdi savunması

**Files:**
- Modify: `backend/services/cv_service.py`
- Test: `tests/test_cv_service.py`

**Interfaces:**
- Consumes: mevcut `analyze_cv`, `_attempt_analysis`, `CVAnalysisError`, `MAX_ATTEMPTS`, `BACKOFF_BASE_SECONDS`, `CVAnalysisOutput` (değişmez).
- Produces:
  - `InvalidCVError(Exception)` — modül düzeyinde.
  - `MIN_CV_TEXT_LENGTH = 40`.
  - `CVAnalysisService._is_effectively_empty(self, result: dict) -> bool`.
  - `analyze_cv`: Katman 1 (uzunluk) + Katman 2 (etkin-boş) ile `InvalidCVError` fırlatır; aksi halde eskisi gibi doğrulanmış dict döner.

- [ ] **Step 1: Testleri güncelle ve yeni testleri ekle**

`tests/test_cv_service.py`'de import satırını güncelle:

```python
from services.cv_service import CVAnalysisService, CVAnalysisError, InvalidCVError
```

`_VALID_OUTPUT` tanımının hemen ALTINA iki sabit ekle:

```python
# Katman 1 uzunluk kontrolunu (MIN_CV_TEXT_LENGTH=40) gecen, gecerli uzunlukta ornek girdi.
_CV_TEXT = "Ahmet Yilmaz, Backend Developer. Python, FastAPI ve PostgreSQL deneyimi var."

# Modelin 'bu bir CV degil' sinyali: tum alanlar bos/0.
_EMPTY_OUTPUT = {
    "skills": [],
    "experience_years": 0.0,
    "education": [],
    "strengths": [],
    "gaps": [],
    "role_scores": {},
    "top_role_reasons": [],
}
```

Mevcut testlerdeki kısa girdileri `_CV_TEXT` ile değiştir (Katman 1 artık kısa girdiyi reddediyor):
- `test_gecerli_cikti_dict_doner` içinde `service.analyze_cv("herhangi bir CV metni")` → `service.analyze_cv(_CV_TEXT)`
- `test_semaya_uymayan_cikti_CVAnalysisError_verir` içinde `service.analyze_cv("herhangi bir CV metni")` → `service.analyze_cv(_CV_TEXT)`
- `test_api_hatasi_sonra_basari` içinde `service.analyze_cv("CV")` → `service.analyze_cv(_CV_TEXT)`
- `test_cikti_hatasi_beklemeden_tekrar_dener` içinde `service.analyze_cv("CV")` → `service.analyze_cv(_CV_TEXT)`
- `test_uc_deneme_de_basarisiz_CVAnalysisError` içinde `service.analyze_cv("CV")` → `service.analyze_cv(_CV_TEXT)`

Dosyanın SONUNA 3 yeni test ekle:

```python
def test_cok_kisa_girdi_gemini_cagirmadan_InvalidCVError(monkeypatch):
    service = _make_service(monkeypatch, [json.dumps(_VALID_OUTPUT)])

    with pytest.raises(InvalidCVError):
        service.analyze_cv("Merhaba dunya")  # 40 karakterden kisa

    # Katman 1 API'siz olmali: generate_content hic cagrilmamali
    assert service.client.models.calls == 0


def test_bos_girdi_gemini_cagirmadan_InvalidCVError(monkeypatch):
    service = _make_service(monkeypatch, [json.dumps(_VALID_OUTPUT)])

    with pytest.raises(InvalidCVError):
        service.analyze_cv("   ")

    assert service.client.models.calls == 0


def test_etkin_bos_cikti_InvalidCVError(monkeypatch):
    # Yeterince uzun ama CV olmayan metin -> Gemini'ye gider; model bos dondurur
    non_cv = "Bu bir yemek tarifidir: un, seker ve yumurtayi bir kapta karistirin."
    service = _make_service(monkeypatch, [json.dumps(_EMPTY_OUTPUT)])

    with pytest.raises(InvalidCVError):
        service.analyze_cv(non_cv)

    assert service.client.models.calls == 1  # analiz denendi, sonuc bos -> InvalidCVError
```

- [ ] **Step 2: Testleri çalıştır, `InvalidCVError` tanımsız olduğu için başarısız olduklarını doğrula**

Run: `./venv/Scripts/python.exe -m pytest tests/test_cv_service.py -q`
Expected: FAIL — `ImportError: cannot import name 'InvalidCVError' from 'services.cv_service'` (tüm modül import hatası verir).

- [ ] **Step 3: `cv_service.py`'de `InvalidCVError` + sabit + prompt kuralı + yardımcı + `analyze_cv` güncellemesi**

**(3a)** `CVAnalysisError` sınıfı ve `MAX_ATTEMPTS`/`BACKOFF_BASE_SECONDS` sabitlerinin bulunduğu bloğa, sabitlerden SONRA ekle:

```python
class InvalidCVError(Exception):
    """Girdi metninin gecerli bir CV olmadigini belirtir (cok kisa/bos veya alakasiz belge)."""


MIN_CV_TEXT_LENGTH = 40
```

**(3b)** `_attempt_analysis` içindeki `system_instruction`'da şu iki satırı bul:

```python
            "ÖNEMLİ KURALLAR:\n"
            "1. Deneyim yılını sayısal (float) olarak çıkar.\n"
```

ve aralarına rule 0'ı ekleyerek şununla değiştir:

```python
            "ÖNEMLİ KURALLAR:\n"
            "0. ÖNCE metnin bir CV/özgeçmiş olup olmadığını değerlendir. Metin bir CV DEĞİLSE "
            "(örn. tarif, haber, makale, rastgele metin), aşağıdaki kuralları UYGULAMA ve TÜM "
            "alanları boş/0 döndür: skills=[], experience_years=0, education=[], strengths=[], "
            "gaps=[], role_scores'ta tüm roller 0, top_role_reasons=[].\n"
            "1. Deneyim yılını sayısal (float) olarak çıkar.\n"
```

**(3c)** `CVAnalysisService` sınıfı içine, `analyze_cv`'nin hemen ÜSTÜNE yeni yardımcı metodu ekle:

```python
    def _is_effectively_empty(self, result: dict) -> bool:
        """Model, metnin CV olmadigini bos/0 ciktiyla sinyalledi mi?

        skills bos VE tum role_scores 0 ise etkin bos sayilir (muhafazakar AND).
        """
        if result.get("skills"):
            return False
        role_scores = result.get("role_scores") or {}
        return all(score == 0 for score in role_scores.values())
```

**(3d)** Mevcut `analyze_cv` metodunu **tamamen** aşağıdakiyle değiştir:

```python
    def analyze_cv(self, cv_text: str) -> dict:
        """Ham CV metnini analiz eder; gecersiz girdide InvalidCVError firlatir.

        Katman 1 (API'siz): cok kisa/bos girdi -> InvalidCVError.
        Retry + sema dogrulama: gecici hatada tekrar dener (bkz. CVAnalysisError).
        Katman 2: model CV olmadigini bos ciktiyla sinyallerse -> InvalidCVError.
        """
        # Katman 1: Python uzunluk kontrolu (Gemini cagrilmaz)
        if not cv_text or len(cv_text.strip()) < MIN_CV_TEXT_LENGTH:
            raise InvalidCVError(
                "Girdi cok kisa veya bos; gecerli bir CV olarak analiz edilemez."
            )

        last_error: Exception | None = None
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                result = self._attempt_analysis(cv_text)
            except (json.JSONDecodeError, ValidationError) as output_err:
                # Model bir sonraki denemede duzgun JSON/sema uretebilir; beklemeden dene
                last_error = output_err
                continue
            except Exception as api_err:
                # Gecici API hatasi: artan bekleme sonra tekrar dene
                last_error = api_err
                if attempt < MAX_ATTEMPTS:
                    time.sleep(BACKOFF_BASE_SECONDS * attempt)
                continue

            # Katman 2: model metnin CV olmadigini bos ciktiyla sinyalledi mi?
            if self._is_effectively_empty(result):
                raise InvalidCVError(
                    "Metin bir CV gibi analiz edilemedi (alakasiz belge olabilir)."
                )
            return result

        raise CVAnalysisError(
            f"CV analizi {MAX_ATTEMPTS} denemede başarısız: {last_error}"
        ) from last_error
```

Not: `except` dallarındaki `continue` ZORUNLU — başarısız denemede `result` tanımsız kalır; `continue` olmadan Katman 2 kontrolüne düşüp `NameError` verir.

- [ ] **Step 4: Testleri çalıştır, geçtiklerini doğrula**

Run: `./venv/Scripts/python.exe -m pytest tests/test_cv_service.py -v`
Expected: PASS — 8 test (5 güncellenmiş + 3 yeni) geçer.

- [ ] **Step 5: Tüm offline suite'i doğrula**

Run: `./venv/Scripts/python.exe -m pytest -q`
Expected: PASS — 15 (cv_parser) + 8 (cv_service) = 23 passed.

- [ ] **Step 6: COMMIT YAPMA**

Commit YOK. Değişiklikleri çalışma ağacında bırak. Rapora `git diff --stat` ekle. (Kontrolör inceleme sonrası commit'leyecek.)

---

## Self-Review Notu

- **Spec kapsamı:** InvalidCVError ✓ (3a), Katman 1 uzunluk ✓ (3d başı), Katman 2 prompt kuralı ✓ (3b) + etkin-boş kontrolü ✓ (3c+3d), retry dışında ✓ (Katman 2 döngü içi ama başarılı sonuçtan sonra, `continue`'larla ayrılmış), etkin-boş kriteri `skills=[] ve tüm role_scores=0` ✓ (3c), MIN_CV_TEXT_LENGTH=40 ✓, şema değişmedi ✓.
- **Mevcut test etkileşimi:** Katman 1'in kısa girdiyi reddetmesi mevcut testleri kıracağı için girdileri `_CV_TEXT` ile güncellemek Step 1'e dahil edildi.
- **Placeholder yok:** her adımda tam kod/komut.
- **Tip tutarlılığı:** `InvalidCVError`, `MIN_CV_TEXT_LENGTH`, `_is_effectively_empty`, `_CV_TEXT`, `_EMPTY_OUTPUT`, `analyze_cv`, `_attempt_analysis` her yerde tutarlı.
- **TDD:** Yeni davranış (uzunluk + etkin-boş tespiti) deterministik Python olduğu için gerçek failing-test → pass döngüsü uygulanır (Madde 1'in aksine offline test edilebilir).
