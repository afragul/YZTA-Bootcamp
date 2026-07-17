"""
Tum eval scriptlerinin ORTAK YOL AYARI.

Her eval scriptinin en ustunde su blok olacak:

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo koku

    from evals._paths import BACKEND, TEST_RESULTS, LEARNING_PLANS

Bu dosya iki is yapiyor:
  1) backend/ klasorunu sys.path'e ekler
     -> 'from services.cv_service import ...' calisir
  2) TUM yollari mutlak (absolute) hale getirir
     -> scripti NEREDEN calistirirsan calistir dogru dosyayi bulur

Klasor yapisi degisirse SADECE BU DOSYA guncellenir, 4 script'e dokunulmaz.
"""

import os
import sys

# --- Temel dizinler ---
EVALS = os.path.dirname(os.path.abspath(__file__))   # .../YZTA-Bootcamp/evals
ROOT = os.path.dirname(EVALS)                        # .../YZTA-Bootcamp

# --- Urun kodu (Kisi 1/2/4'un alani - sadece OKUYORUZ) ---
BACKEND = os.path.join(ROOT, "backend")

# --- Girdi verileri (Kisi 2'nin - sadece OKUYORUZ) ---
SAMPLE_CVS = os.path.join(ROOT, "sample_cvs")
TEST_RESULTS = os.path.join(ROOT, "test_results")

# --- Bizim urettigimiz kanitlar (YAZIYORUZ) ---
RESULTS = os.path.join(EVALS, "results")
SCORING_RESULTS = os.path.join(RESULTS, "scoring")
LEARNING_PLANS = os.path.join(RESULTS, "learning", "plans")

# --- backend'i import edilebilir yap ---
if BACKEND not in sys.path:
    sys.path.insert(0, BACKEND)

# --- Cikti klasorleri yoksa olustur ---
os.makedirs(SCORING_RESULTS, exist_ok=True)
os.makedirs(LEARNING_PLANS, exist_ok=True)