"""
top_role_reasons tutarlilik eval'i — 0 Gemini cagrisi.

Kayitli analiz ciktilari (test_results/*.json) uzerinden calisir, kota harcamaz.
Her gerekce kaydi icin uc sey dogrulanir:

  1. isim_ok    : 'role' adi role_scores'ta GERCEKTEN var mi? (AI rol uydurmus olabilir)
  2. skor_ok    : 'score' degeri role_scores'taki puanla ayni mi? (AI farkli puan yazabilir)
  3. gerekce_ok : 'reason' dolu mu? (30 karakterden uzun)

Ayrica gerekce alani hic bulunmayan dosyalar ayri raporlanir; bunlar
top_role_reasons semaya eklenmeden ONCE uretilmis eski ciktilardir ve
yeniden uretilmedikce bu eval tarafindan kontrol edilemezler.

Sonuc evals/results/scoring/reasons.json dosyasina yazilir.
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from evals._paths import SCORING_RESULTS, TEST_RESULTS

# Gerekcenin "dolu" sayilmasi icin gereken en az karakter sayisi
MIN_GEREKCE_UZUNLUGU = 30


def main():
    kayitlar = []          # her gerekce icin bir satir
    eksik_alanli_dosyalar = []  # top_role_reasons hic olmayan dosyalar

    for fname in sorted(os.listdir(TEST_RESULTS)):
        if not fname.endswith(".json"):
            continue

        with open(os.path.join(TEST_RESULTS, fname), "r", encoding="utf-8") as f:
            data = json.load(f)

        print("=" * 70)
        print(f"DOSYA: {fname}")

        scores = data.get("role_scores", {})
        reasons = data.get("top_role_reasons", [])

        if not reasons:
            print("  HATA: top_role_reasons alani BOS veya YOK!")
            print("        (bu cikti, alan semaya eklenmeden once uretilmis)")
            eksik_alanli_dosyalar.append(fname)
            continue

        # Gerekceler gercekten en yuksek 3 role mi ait? (bilgi amacli)
        gercek_top3 = [r for r, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]]
        print(f"  Skorlara gore gercek top 3: {gercek_top3}")

        for r in reasons:
            rol = r.get("role")
            skor = r.get("score")
            gerekce = r.get("reason", "")

            isim_ok = rol in scores
            skor_ok = isim_ok and scores[rol] == skor
            gerekce_ok = len(gerekce) > MIN_GEREKCE_UZUNLUGU
            gecti = isim_ok and skor_ok and gerekce_ok

            print(f"\n  [{'OK' if gecti else 'SORUN'}] {rol} = {skor}")
            if not isim_ok:
                print("      -> ROL ADI role_scores'ta YOK (AI uydurmus!)")
            if isim_ok and not skor_ok:
                print(f"      -> SKOR UYUSMUYOR (role_scores'ta: {scores[rol]})")
            if not gerekce_ok:
                print("      -> GEREKCE COK KISA / BOS")
            print(f"      Gerekce: {gerekce}")

            kayitlar.append(
                {
                    "dosya": fname,
                    "rol": rol,
                    "skor": skor,
                    "gercek_top3_te_mi": rol in gercek_top3,
                    "isim_ok": isim_ok,
                    "skor_ok": skor_ok,
                    "gerekce_ok": gerekce_ok,
                    "sonuc": "GECTI" if gecti else "KALDI",
                    "gerekce": gerekce,
                }
            )

    # --- Ozet ---
    toplam = len(kayitlar)
    gecen = sum(1 for k in kayitlar if k["sonuc"] == "GECTI")
    oran = (gecen / toplam * 100) if toplam else 0.0

    print("\n" + "=" * 70)
    print(f"KONTROL EDILEN GEREKCE : {toplam}")
    print(f"GECEN                  : {gecen}  (%{oran:.0f})")
    if eksik_alanli_dosyalar:
        print(f"GEREKCE ALANI BOS      : {len(eksik_alanli_dosyalar)} dosya "
              f"-> {', '.join(eksik_alanli_dosyalar)}")
        print("  Bu dosyalar kontrole DAHIL DEGIL. Kapsama almak icin")
        print("  'python run_cv_tests.py' ile yeniden uretilmeleri gerekir (canli Gemini).")
    print("=" * 70)

    # --- Sunumda kullanmak icin diske yaz ---
    cikti_yolu = os.path.join(SCORING_RESULTS, "reasons.json")
    with open(cikti_yolu, "w", encoding="utf-8") as f:
        json.dump(
            {
                "basari_orani": round(oran, 1),
                "kontrol_edilen_gerekce": toplam,
                "gecen": gecen,
                "gerekce_alani_bos_dosyalar": eksik_alanli_dosyalar,
                "kontrol_edilen_dosya_sayisi": len({k["dosya"] for k in kayitlar}),
                "detay": kayitlar,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    print(f"\nDetayli sonuc: {os.path.basename(cikti_yolu)}")


if __name__ == "__main__":
    main()
