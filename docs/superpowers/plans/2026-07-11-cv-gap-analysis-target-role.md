# Hedef Role Göre Eksik Analizi Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `analyze_cv` promptunun `gaps` üretimini genel yerine adayın en yüksek 3 `role_scores` rolüne göre, rol etiketli ve CV kanıtına dayalı hale getirmek.

**Architecture:** Tek dosyada, tek stringde bir prompt düzenlemesi. `cv_service._attempt_analysis` içindeki `system_instruction`'ın 4. maddesi güncellenir. Şema, imza, dönüş tipi ve retry mantığı değişmez; `gaps` hâlâ `list[str]`.

**Tech Stack:** Python, `google-genai` (Gemini `gemini-2.5-flash`), mevcut `system_instruction` string'i.

## Global Constraints

- **Şemaya DOKUNMA** — `CVAnalysisOutput` dondurulmuş ekip kontratı; `gaps` tipi `list[str]` kalır. Değişiklik yalnızca prompt metnindedir.
- **Yalnızca `system_instruction` madde 4 değişir** — madde 5–7 (skorlama cetveli, top_role_reasons) ve `_attempt_analysis`'in geri kalanı korunur.
- **`strengths`'e dokunma** — bu iş sadece `gaps` hakkında.
- **Yorum/prompt metni Türkçe** — mevcut dosya konvansiyonu.
- **Yeni bağımlılık yok.**
- **Offline regresyon:** mevcut 20 test (`cv_parser` 15 + `cv_service` 5) yeşil kalmalı. Python: `./venv/Scripts/python.exe`.
- **İçerik kalitesi offline test edilemez** (LLM, sahte client). Kalite doğrulaması canlı `run_cv_tests.py` iledir.

---

## File Structure

- **Modify:** `backend/services/cv_service.py` — `_attempt_analysis` içindeki `system_instruction` string'inin 4. maddesi (tek satırlık string, çok satırlı yönergeyle değiştirilir).

Yeni dosya yok, yeni test dosyası yok. Bu bir prompt kalite değişikliği olduğundan içeriğe dair offline birim testi eklenmez (LLM çıktısı deterministik değil; sahte-client testi yalnızca prompt metnini tekrar yazan, hiçbir davranış doğrulamayan kırılgan bir test olur — bilinçli olarak eklenmez). Mevcut suite regresyon güvencesi olarak kullanılır.

---

## Task 1: `gaps`'i hedef role göre üreten prompt güncellemesi

**Files:**
- Modify: `backend/services/cv_service.py` (`_attempt_analysis` içindeki `system_instruction`, 4. madde)

**Interfaces:**
- Consumes: mevcut `system_instruction` string'i, `CVAnalysisOutput.gaps: list[str]` (değişmez).
- Produces: davranış değişikliği yok (imza/tip sabit); yalnızca `gaps` içeriğinin niteliği değişir. Dış arayüz aynı kalır.

- [ ] **Step 1: Mevcut 4. maddeyi yeni çok satırlı yönergeyle değiştir**

`backend/services/cv_service.py` içinde, `_attempt_analysis` metodundaki `system_instruction` string'inde şu tam satırı bul:

```python
            "4. Adayın güçlü yönlerini (strengths) ve gelişim alanlarını (gaps) net maddeler halinde belirt.\n"
```

ve **tamamen** aşağıdakiyle değiştir:

```python
            "4. İki liste üret:\n"
            "   - strengths: adayın genel güçlü yönlerini net maddeler halinde belirt.\n"
            "   - gaps: adayın EN YÜKSEK skorlu 3 rolü için (aşağıda role_scores'ta en yüksek "
            "puanı verdiğin 3 rol) eksik veya zayıf yönleri belirt. Her gap maddesi "
            "'[Rol Görünen Adı] eksik/zayıf nokta' biçiminde başlamalı "
            "(örn. '[Machine Learning Engineer] Üretim ortamında model dağıtımı (MLOps) deneyimi yok'). "
            "Her eksiği CV'deki SOMUT kanıta dayandır (eksik beceri/araç/proje deneyimi); "
            "tahmin veya varsayımda bulunma. Rol etiketleri role_scores'taki en yüksek rollerle "
            "TUTARLI olmalı. Her rol için en önemli 1-3 eksiği yaz; liste kısa ve eyleme dönük kalsın.\n"
```

Not: Bu bir string birleştirme (`(...)` içinde ardışık string literalleri) bloğudur; yeni satırlar Python tarafından tek string'e birleştirilir. Girinti ve tırnak kapanışlarını mevcut madde 5/6/7 stiliyle aynı tut.

- [ ] **Step 2: Dosyanın hâlâ import edilebildiğini ve app'in açıldığını doğrula**

Run: `./venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'backend'); from main import app; from services.cv_service import CVAnalysisService; print('import OK')"`
Expected: `import OK` (syntax/string hatası yoksa). Prompt string'inde kaçış veya tırnak hatası olursa burada `SyntaxError` alınır.

- [ ] **Step 3: Offline regresyon suite'inin yeşil kaldığını doğrula**

Run: `./venv/Scripts/python.exe -m pytest -q`
Expected: `20 passed`. (Prompt değişikliği `gaps` tipini değiştirmediği için sahte-client testleri etkilenmez; bu adım değişikliğin hiçbir şeyi bozmadığını kanıtlar.)

- [ ] **Step 4: (Canlı doğrulama — GEMINI_API_KEY + kota gerektirir) `gaps`'in artık rol etiketli geldiğini göz kontrolüyle teyit et**

Run (kök dizinde): `python run_cv_tests.py`
Sonra `test_results/*.json` dosyalarındaki `gaps` alanına bak. Beklenen: her CV için gaps maddeleri `[Rol Adı] ...` biçiminde başlıyor, o CV'nin en yüksek 3 rolüne atıfta bulunuyor ve etiketler `role_scores`'taki en yüksek rollerle tutarlı. Örn. `cv_devops.txt` çıktısında `[DevOps Engineer] ...`, `[Cloud Engineer] ...` gibi maddeler.

Not: Bu adım canlı Gemini çağırır (kota harcar) ve deterministik değildir; otomatik bir assert değil, insan göz kontrolüdür. CI'da çalıştırılmaz. `GEMINI_API_KEY` yoksa bu adım atlanır ve doğrulama Step 3'ün regresyon güvencesiyle sınırlı kalır.

- [ ] **Step 5: Commit**

```bash
git add backend/services/cv_service.py
git commit -m "feat(ai-core): gaps'i hedef role gore uret (rol etiketli)

analyze_cv promptu (madde 4) artik gaps'i adayin en yuksek 3 role gore,
'[Rol Adi] ...' etiketli ve CV kanitina dayali uretiyor. gaps tipi
list[str] korundu; sema/imza degismedi. Offline suite: 20 passed.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Self-Review Notu

- **Spec kapsamı:** hedef rol = en yüksek 3 role_scores ✓ (Step 1 metni), temsil = düz list[str] + rol etiketi ✓, yalnızca prompt madde 4 ✓, strengths dokunulmadı ✓ (madde 4 içinde korundu), bağımsızlık = şema değişmedi ✓, doğrulama = offline regresyon (Step 3) + canlı run_cv_tests (Step 4) ✓.
- **Placeholder yok:** Step 1 tam eski/yeni string'i, Step 2–4 tam komutları içeriyor.
- **Tip tutarlılığı:** `gaps: list[str]`, `system_instruction`, `_attempt_analysis`, `run_cv_tests.py`, `./venv/Scripts/python.exe` her adımda tutarlı.
- **TDD notu:** Prompt kalite değişikliği olduğundan içerik için offline "failing test → pass" döngüsü uygulanamaz; bunun yerine Step 3 regresyon güvencesi + Step 4 canlı göz doğrulaması kullanılır. Bu, spec'in "Doğrulama" bölümüyle birebir uyumludur.
