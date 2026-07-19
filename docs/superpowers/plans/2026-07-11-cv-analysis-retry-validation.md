# analyze_cv Retry + Pydantic Doğrulama Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `CVAnalysisService.analyze_cv`'yi 3 denemelik retry + Pydantic şema doğrulaması ile sağlamlaştır; başarıda doğrulanmış dict döndür, tükenince `CVAnalysisError` fırlat.

**Architecture:** Tek Gemini çağrısı + parse + doğrulama bir yardımcı metoda (`_attempt_analysis`) alınır; `analyze_cv` bunu saran retry döngüsü olur. Hatalar iki sınıfa ayrılır: çıktı/şema hataları (beklemeden tekrar dene) ve API hataları (artan bekleme). Yeni bağımlılık yok.

**Tech Stack:** Python 3.13, `google-genai`, `pydantic>=2`, `pytest` (offline testler, sahte client).

## Global Constraints

- **Yeni PyPI bağımlılığı ekleme** — yalnızca hâlihazırda kurulu paketler (`google-genai`, `pydantic`, `pytest`, stdlib).
- **Kod yorumları, docstring'ler ve hata mesajları Türkçe** — mevcut dosya konvansiyonu.
- **Testler tamamen offline** — gerçek Gemini çağrısı yok, `GEMINI_API_KEY` gerektirmez, kota harcamaz. Sahte client + `monkeypatch` kullanılır.
- **`pytest` kök dizinden çalışır** (`pytest.ini` → `pythonpath = backend`, `testpaths = tests`). Modül yolu `services.cv_service`.
- **`analyze_cv` dönüş tipi dict kalır** (`model_dump()`) — `run_cv_tests.py` / `test_prompt.py` bozulmamalı.
- Sabitler: `MAX_ATTEMPTS = 3`, `BACKOFF_BASE_SECONDS = 1.0` (deneme *k* sonrası bekleme `BACKOFF_BASE_SECONDS * k`).

---

## File Structure

- **Modify:** `backend/services/cv_service.py` — `CVAnalysisError` istisnası, `import time` + `from pydantic import ValidationError`, `_attempt_analysis` yardımcı metodu, `analyze_cv` retry döngüsü, `MAX_ATTEMPTS`/`BACKOFF_BASE_SECONDS` sabitleri.
- **Create:** `tests/test_cv_service.py` — sahte client altyapısı + offline davranış testleri.

---

## Task 1: Çıktı doğrulama + `CVAnalysisError` + dict dönüş (retry yok)

**Files:**
- Modify: `backend/services/cv_service.py`
- Test: `tests/test_cv_service.py`

**Interfaces:**
- Consumes: `schemas.cv_analysis.CVAnalysisOutput` (mevcut Pydantic modeli), `CVAnalysisService.client` (Gemini client, testte sahte ile değiştirilir).
- Produces:
  - `CVAnalysisError(Exception)` — modül düzeyinde istisna.
  - `CVAnalysisService._attempt_analysis(self, cv_text: str) -> dict` — tek Gemini çağrısı + `json.loads` + `CVAnalysisOutput(**data)` doğrulaması, `validated.model_dump()` döndürür; hataları yakalamaz.
  - `CVAnalysisService.analyze_cv(self, cv_text: str) -> dict` — `_attempt_analysis`'i çağırır; bu aşamada herhangi bir exception'ı `CVAnalysisError`'a çevirir.

- [ ] **Step 1: Test dosyasını sahte client altyapısı + iki testle oluştur**

Create `tests/test_cv_service.py`:

```python
"""CVAnalysisService retry + dogrulama testleri (Kisi 2).

Gemini API cagirmaz; sahte client ile tamamen offline calisir.
"""
import json

import pytest

from services.cv_service import CVAnalysisService, CVAnalysisError


# Semaya uygun minimal gecerli analiz JSON'u.
# role_scores {} birakilir -> Pydantic 22 rolu 0 default ile doldurur.
_VALID_OUTPUT = {
    "skills": ["Python", "FastAPI"],
    "experience_years": 3.0,
    "education": [],
    "strengths": ["Guclu backend temeli"],
    "gaps": ["Docker deneyimi az"],
    "role_scores": {},
}


class _FakeResponse:
    def __init__(self, text: str):
        self.text = text


class _FakeModels:
    """generate_content her cagrildiginda outcomes'tan sirayla bir oge tuketir.

    Oge str ise .text olarak doner; Exception ornegi ise firlatilir.
    """

    def __init__(self, outcomes):
        self._outcomes = list(outcomes)
        self.calls = 0

    def generate_content(self, **kwargs):
        self.calls += 1
        outcome = self._outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return _FakeResponse(outcome)


class _FakeClient:
    def __init__(self, outcomes):
        self.models = _FakeModels(outcomes)


def _make_service(monkeypatch, outcomes) -> CVAnalysisService:
    """API anahtarini sahteleyip servisi kurar, client'i sahte ile degistirir."""
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    service = CVAnalysisService()
    service.client = _FakeClient(outcomes)
    return service


def test_gecerli_cikti_dict_doner(monkeypatch):
    service = _make_service(monkeypatch, [json.dumps(_VALID_OUTPUT)])

    result = service.analyze_cv("herhangi bir CV metni")

    assert isinstance(result, dict)
    assert result["skills"] == ["Python", "FastAPI"]
    assert result["experience_years"] == 3.0
    # role_scores bos gelse de sema tum 22 rolu 0 ile doldurur
    assert result["role_scores"]["backend_developer"] == 0
    assert service.client.models.calls == 1


def test_semaya_uymayan_cikti_CVAnalysisError_verir(monkeypatch):
    # experience_years zorunlu; eksik birakmak Pydantic ValidationError uretir
    bad = json.dumps({"skills": []})
    service = _make_service(monkeypatch, [bad, bad, bad])

    with pytest.raises(CVAnalysisError):
        service.analyze_cv("herhangi bir CV metni")
```

- [ ] **Step 2: Testleri çalıştır, import hatasıyla başarısız olduklarını doğrula**

Run: `./venv/Scripts/python.exe -m pytest tests/test_cv_service.py -v`
Expected: FAIL — `ImportError: cannot import name 'CVAnalysisError' from 'services.cv_service'` (henüz tanımlı değil).

- [ ] **Step 3: `cv_service.py`'ye `CVAnalysisError` + `_attempt_analysis` ekle, `analyze_cv`'yi sadeleştir**

`backend/services/cv_service.py` içinde, importların hemen altına (satır 6'dan sonra) istisnayı ekle:

```python
from schemas.cv_analysis import CVAnalysisOutput


class CVAnalysisError(Exception):
    """CV analizinin (Gemini cagrisi + JSON parse + sema dogrulama) basarisiz oldugunu belirtir."""
```

`analyze_cv` metodunu (mevcut satır 62-102) **tamamen** aşağıdakiyle değiştir. `system_instruction` bloğu birebir korunur, sadece Gemini çağrısı + parse + doğrulama `_attempt_analysis`'e taşınır:

```python
    def _attempt_analysis(self, cv_text: str) -> dict:
        """Tek bir Gemini cagrisi yapar, ciktiyi semaya gore dogrular, dict dondurur.

        Cagri / JSON parse / dogrulama hatalarini YAKALAMAZ; retry mantigi
        analyze_cv'ye aittir. Basarili donus her zaman CVAnalysisOutput semasina
        uygun bir dict'tir.
        """
        response_schema = self._get_clean_schema()

        # Yapay zekaya 22 rolun tamamini analiz etmesini soyleyen sistem talimati
        system_instruction = (
            "Sen profesyonel bir Kariyer ve İK Asistanı yapay zekasısın. Görevin, sana verilen "
            "CV metnini titizlikle incelemek ve belirtilen JSON şemasına uygun şekilde analiz etmektir.\n\n"
            "ÖNEMLİ KURALLAR:\n"
            "1. Deneyim yılını sayısal (float) olarak çıkar.\n"
            "2. Eğitim geçmişini listele.\n"
            "3. Adayın sahip olduğu teknik, sektörel ve sosyal (soft skills) becerilerini listele.\n"
            "4. Adayın güçlü yönlerini (strengths) ve gelişim alanlarını (gaps) net maddeler halinde belirt.\n"
            "5. 'role_scores' altındaki tüm 22 alan için adayın CV'sine göre 0-100 arasında uygunluk skoru ata:\n"
            "   - Yazılım Geliştirme: backend_developer, frontend_developer, fullstack_developer, mobile_developer, devops_engineer, cloud_engineer\n"
            "   - Veri & AI Sistemleri: machine_learning_engineer, data_scientist, data_engineer, data_analyst, bi_analyst, database_administrator\n"
            "   - Altyapı & Güvenlik: cybersecurity_specialist, systems_administrator\n"
            "   - Tasarım: ui_ux_designer, graphic_designer\n"
            "   - Yönetim & Analiz: product_manager, project_manager, business_analyst\n"
            "   - İş Operasyonları: digital_marketing_specialist, hr_specialist, customer_success_specialist\n"
            "Her bir alan için kesinlikle sayısal bir puan hesaplamalı ve boş bırakmamalısın."
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=f"Lütfen aşağıdaki CV metnini analiz et ve sonucu dön:\n\n{cv_text}",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=response_schema,
                temperature=0.2,  # Puanlamanın tutarlı olması için düşük sıcaklık
            ),
        )

        data = json.loads(response.text)
        validated = CVAnalysisOutput(**data)
        return validated.model_dump()

    def analyze_cv(self, cv_text: str) -> dict:
        """Ham CV metnini analiz eder, sema-uyumlu dict dondurur.

        (Retry Task 2'de eklenecek.)
        """
        try:
            return self._attempt_analysis(cv_text)
        except Exception as e:
            raise CVAnalysisError(f"CV analizi başarısız: {e}") from e
```

- [ ] **Step 4: Testleri çalıştır, geçtiklerini doğrula**

Run: `./venv/Scripts/python.exe -m pytest tests/test_cv_service.py -v`
Expected: PASS — `test_gecerli_cikti_dict_doner` ve `test_semaya_uymayan_cikti_CVAnalysisError_verir` geçer.

- [ ] **Step 5: Tüm offline suite'in hâlâ yeşil olduğunu doğrula**

Run: `./venv/Scripts/python.exe -m pytest -q`
Expected: PASS — mevcut `cv_parser` testleri (15) + yeni 2 test = 17 passed.

- [ ] **Step 6: Commit**

```bash
git add backend/services/cv_service.py tests/test_cv_service.py
git commit -m "feat(ai-core): analyze_cv Pydantic dogrulama + CVAnalysisError

Cikti CVAnalysisOutput ile dogrulaniyor, sema-uyumlu dict donuyor;
ham Gemini/JSON/validation hatasi tek CVAnalysisError'a cevriliyor.
Retry Task 2'de.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 2: Retry döngüsü (API hatası → backoff, çıktı hatası → beklemeden)

**Files:**
- Modify: `backend/services/cv_service.py`
- Test: `tests/test_cv_service.py`

**Interfaces:**
- Consumes: `CVAnalysisService._attempt_analysis` (Task 1), `CVAnalysisError` (Task 1).
- Produces: `analyze_cv` artık en fazla `MAX_ATTEMPTS` (3) deneme yapar; `json.JSONDecodeError`/`ValidationError`'da beklemeden, diğer exception'larda `BACKOFF_BASE_SECONDS * attempt` bekledikten sonra tekrar dener; tümü tükenince `CVAnalysisError` fırlatır. Dönüş tipi dict korunur.

- [ ] **Step 1: Retry davranış testlerini ekle**

`tests/test_cv_service.py` sonuna ekle:

```python
def test_api_hatasi_sonra_basari(monkeypatch):
    sleeps = []
    monkeypatch.setattr("services.cv_service.time.sleep", lambda s: sleeps.append(s))
    err = RuntimeError("gecici API hatasi (429)")
    service = _make_service(monkeypatch, [err, json.dumps(_VALID_OUTPUT)])

    result = service.analyze_cv("CV")

    assert result["skills"] == ["Python", "FastAPI"]
    assert service.client.models.calls == 2
    assert sleeps == [1.0]  # ilk denemeden sonra 1sn beklendi


def test_cikti_hatasi_beklemeden_tekrar_dener(monkeypatch):
    sleeps = []
    monkeypatch.setattr("services.cv_service.time.sleep", lambda s: sleeps.append(s))
    bad = json.dumps({"skills": []})  # ValidationError -> cikti hatasi
    service = _make_service(monkeypatch, [bad, json.dumps(_VALID_OUTPUT)])

    result = service.analyze_cv("CV")

    assert result["experience_years"] == 3.0
    assert service.client.models.calls == 2
    assert sleeps == []  # cikti hatasinda beklenmez


def test_uc_deneme_de_basarisiz_CVAnalysisError(monkeypatch):
    monkeypatch.setattr("services.cv_service.time.sleep", lambda s: None)
    err = RuntimeError("kalici API hatasi")
    service = _make_service(monkeypatch, [err, err, err])

    with pytest.raises(CVAnalysisError):
        service.analyze_cv("CV")

    assert service.client.models.calls == 3
```

- [ ] **Step 2: Testleri çalıştır, retry olmadığı için başarısız olduklarını doğrula**

Run: `./venv/Scripts/python.exe -m pytest tests/test_cv_service.py -k "api_hatasi_sonra_basari or cikti_hatasi_beklemeden or uc_deneme" -v`
Expected: FAIL — örn. `test_api_hatasi_sonra_basari` `CVAnalysisError` alır / `calls == 1` olur (henüz retry yok).

- [ ] **Step 3: `import time` + `ValidationError` importunu ekle**

`backend/services/cv_service.py` en üstteki importlara ekle:

```python
import os
import json
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import ValidationError
from schemas.cv_analysis import CVAnalysisOutput
```

Sabitleri `CVAnalysisError` tanımının hemen altına ekle:

```python
MAX_ATTEMPTS = 3
BACKOFF_BASE_SECONDS = 1.0
```

- [ ] **Step 4: `analyze_cv`'yi retry döngüsüyle değiştir**

Task 1'deki `analyze_cv` gövdesini **tamamen** aşağıdakiyle değiştir (`_attempt_analysis` dokunulmaz):

```python
    def analyze_cv(self, cv_text: str) -> dict:
        """Ham CV metnini analiz eder; retry + sema dogrulama ile saglam dict dondurur.

        En fazla MAX_ATTEMPTS deneme yapar:
          - Cikti hatasi (bozuk JSON / semaya uymayan) -> beklemeden tekrar dener.
          - API hatasi (timeout / 429 / 5xx vb.) -> artan bekleme sonra tekrar dener.
        Tum denemeler tukenirse CVAnalysisError firlatir (orijinal sebep zincirlenir).
        """
        last_error: Exception | None = None
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                return self._attempt_analysis(cv_text)
            except (json.JSONDecodeError, ValidationError) as output_err:
                # Model bir sonraki denemede duzgun JSON/sema uretebilir; beklemeden dene
                last_error = output_err
            except Exception as api_err:
                # Gecici API hatasi: artan bekleme sonra tekrar dene
                last_error = api_err
                if attempt < MAX_ATTEMPTS:
                    time.sleep(BACKOFF_BASE_SECONDS * attempt)

        raise CVAnalysisError(
            f"CV analizi {MAX_ATTEMPTS} denemede başarısız: {last_error}"
        ) from last_error
```

- [ ] **Step 5: Testleri çalıştır, geçtiklerini doğrula**

Run: `./venv/Scripts/python.exe -m pytest tests/test_cv_service.py -v`
Expected: PASS — 5 test (Task 1'in 2'si + Task 2'nin 3'ü) geçer.

- [ ] **Step 6: Tüm offline suite'i doğrula**

Run: `./venv/Scripts/python.exe -m pytest -q`
Expected: PASS — 15 (cv_parser) + 5 (cv_service) = 20 passed.

- [ ] **Step 7: Commit**

```bash
git add backend/services/cv_service.py tests/test_cv_service.py
git commit -m "feat(ai-core): analyze_cv 3 denemelik retry + backoff

API hatasinda artan bekleme (1sn->2sn), cikti/sema hatasinda beklemeden
tekrar dener; tukenince CVAnalysisError. Testler sahte client ile offline.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Self-Review Notu

- **Spec kapsamı:** 3 deneme ✓ (Task 2 Step 4), backoff ayrımı ✓, `CVAnalysisError` ✓ (Task 1), dict dönüş ✓ (`model_dump`), offline testler + sahte client + `sleep` patch ✓ (Task 1/2 testleri). Spec'teki 4 test senaryosu → Task 1'de 2, Task 2'de 3 (spec'in "mutlu yol"u Task 1'in `test_gecerli_cikti`'sine karşılık gelir).
- **Placeholder yok:** her adımda gerçek kod/komut var.
- **Tip tutarlılığı:** `_attempt_analysis`, `analyze_cv`, `CVAnalysisError`, `MAX_ATTEMPTS`, `BACKOFF_BASE_SECONDS`, `_FakeClient/_FakeModels/_FakeResponse`, `_make_service`, `_VALID_OUTPUT` her iki görevde aynı adlarla kullanıldı.
