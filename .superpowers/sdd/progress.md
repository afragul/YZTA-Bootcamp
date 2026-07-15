# SDD Progress — geçersiz CV'de güvenli cevap (edge case'ler)

Plan: docs/superpowers/plans/2026-07-11-cv-invalid-input-safe-response.md
Spec: docs/superpowers/specs/2026-07-11-cv-invalid-input-safe-response-design.md
Branch: cv-isleme-ai-analizi
BASE (plan commit'i): ce88995
Baseline: 20 passed

## Görevler
- [x] Task 1: InvalidCVError + iki katmanlı geçersiz-girdi savunması — spec ✅, Approved, 23 passed, COMMIT'siz

## Not
- COMMIT implementer tarafından YAPILMAYACAK (kontrolör/kullanıcı inceledikten sonra).
- Bu görev tamamen offline test edilebilir (deterministik mantık); canlı çalıştırma gerekmez.

## Log
- Task 1: complete — cv_service.py (InvalidCVError, MIN_CV_TEXT_LENGTH=40, prompt rule 0,
  _is_effectively_empty, analyze_cv 2 katman) + test_cv_service.py (import, _CV_TEXT/_EMPTY_OUTPUT,
  5 mevcut test girdisi güncellendi, 3 yeni test). 23 passed. Reviewer spec ✅/Approved.
  Minor (aksiyon gerekmez): _is_effectively_empty staticmethod olabilir; all([]) boş-dict kenar durumu (pratikte zararsız).
- Yan gözlem (görev DIŞI): cv_service.py model_name = "gemini-3.5-flash" BASE'de zaten böyleydi,
  bizim diff'imiz dokunmuyor. Kullanıcıya not düşüldü.
